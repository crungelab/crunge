from __future__ import annotations

from ctypes import c_float, c_uint32, sizeof
from dataclasses import dataclass

import numpy as np
from loguru import logger

from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.engine import Viewport

from .....renderer import Renderer

from ..filter_vu import FilterVu


# --- WGSL: scene draw, kawase blur, composite (fullscreen triangle) ----------------

WGSL = r"""
// Copy/paste WGSL (scene + fullscreen + premultiplied 8-tap blur + composite)
// Branchless bounds masking to satisfy "textureSample must be uniform control flow".

struct VSSceneIn {
  @location(0) pos: vec4f,
  @location(1) color: vec4f,
};

struct VSSceneOut {
  @builtin(position) pos: vec4f,
  @location(0) color: vec4f,
};

@vertex
fn vs_scene(v: VSSceneIn) -> VSSceneOut {
  var o: VSSceneOut;
  o.pos = v.pos;
  o.color = v.color;
  return o;
}

@fragment
fn fs_scene(v: VSSceneOut) -> @location(0) vec4f {
  return v.color;
}

// -----------------------------------------------------------------------------
// Fullscreen triangle

struct VSQuadOut {
  @builtin(position) pos: vec4f,
  @location(0) uv: vec2f,
};

@vertex
fn vs_fullscreen(@builtin(vertex_index) vid: u32) -> VSQuadOut {
  var p = array<vec2f, 3>(
    vec2f(-1.0, -1.0),
    vec2f( 3.0, -1.0),
    vec2f(-1.0,  3.0)
  );

  let pos = p[vid];

  var o: VSQuadOut;
  o.pos = vec4f(pos, 0.0, 1.0);

  // Map clip-space to UV and flip vertically.
  let uv0 = 0.5 * (pos + vec2f(1.0, 1.0));
  o.uv = vec2f(uv0.x, 1.0 - uv0.y);

  return o;
}

// -----------------------------------------------------------------------------
// Shared bindings

@group(0) @binding(0) var src_tex: texture_2d<f32>;
@group(0) @binding(1) var src_samp: sampler;

// -----------------------------------------------------------------------------
// Blur (premultiplied 8-tap Kawase)

struct BlurParams {
  texel_size: vec2f, // (1/width, 1/height)
  offset: f32,       // pixels
  _pad: f32,
};
@group(0) @binding(2) var<uniform> u: BlurParams;

// Returns 1.0 if uv in [0,1]x[0,1], else 0.0. Branchless.
fn in_bounds_mask(uv: vec2f) -> f32 {
  // step(edge, x): 0 if x < edge else 1
  let mx0 = step(0.0, uv.x);
  let mx1 = step(uv.x, 1.0);
  let my0 = step(0.0, uv.y);
  let my1 = step(uv.y, 1.0);
  return mx0 * mx1 * my0 * my1;
}

// Sample, premultiply, and zero-out if out of bounds (branchless).
fn sample_pm_masked(uv: vec2f) -> vec4f {
  let m = in_bounds_mask(uv);
  let c = textureSample(src_tex, src_samp, uv);
  let pm = vec4f(c.rgb * c.a, c.a);
  return pm * m;
}

@fragment
fn fs_kawase(in: VSQuadOut) -> @location(0) vec4f {
  let uv = in.uv;
  let o  = u.offset * u.texel_size;

  var c = vec4f(0.0);

  // Axis taps
  c += sample_pm_masked(uv + vec2f( o.x, 0.0));
  c += sample_pm_masked(uv + vec2f(-o.x, 0.0));
  c += sample_pm_masked(uv + vec2f(0.0,  o.y));
  c += sample_pm_masked(uv + vec2f(0.0, -o.y));

  // Diagonal taps
  c += sample_pm_masked(uv + vec2f( o.x,  o.y));
  c += sample_pm_masked(uv + vec2f(-o.x,  o.y));
  c += sample_pm_masked(uv + vec2f( o.x, -o.y));
  c += sample_pm_masked(uv + vec2f(-o.x, -o.y));

  return c * (1.0 / 8.0); // still premultiplied
}

// -----------------------------------------------------------------------------
// Composite (expects premultiplied input + premultiplied blend state)

struct CompositeParams {
  alpha: f32,
  _pad0: vec3f,
};
@group(0) @binding(3) var<uniform> cu: CompositeParams;

@fragment
fn fs_composite(in: VSQuadOut) -> @location(0) vec4f {
  let c0 = textureSample(src_tex, src_samp, in.uv); // premultiplied blur output
  let a = cu.alpha;
  return vec4f(c0.rgb * a, c0.a * a);
}
"""

# --- CPU-side uniform packing -----------------------------------------------------

@dataclass
class BlurParamsCPU:
    texel_size_x: float
    texel_size_y: float
    offset: float
    _pad: float = 0.0

    def to_bytes(self) -> bytes:
        return np.array(
            [self.texel_size_x, self.texel_size_y, self.offset, self._pad],
            dtype=np.float32,
        ).tobytes()


@dataclass
class CompositeParamsCPU:
    alpha: float
    _pad0: float = 0.0
    _pad1: float = 0.0
    _pad2: float = 0.0

    def to_bytes(self) -> bytes:
        return np.array([self.alpha, self._pad0, self._pad1, self._pad2], dtype=np.float32).tobytes()


# --- Demo ------------------------------------------------------------------------

class KawaseBlurVu(FilterVu):
    vertex_buffer: wgpu.Buffer = None
    index_buffer: wgpu.Buffer = None

    # Offscreen ping-pong
    off_tex_a: wgpu.Texture = None
    off_tex_b: wgpu.Texture = None
    off_view_a: wgpu.TextureView = None
    off_view_b: wgpu.TextureView = None

    # Pipelines
    scene_pipeline: wgpu.RenderPipeline = None
    blur_pipeline: wgpu.RenderPipeline = None
    composite_pipeline: wgpu.RenderPipeline = None

    # Bind group / layout
    blur_bgl: wgpu.BindGroupLayout = None
    blur_pl: wgpu.PipelineLayout = None
    sampler: wgpu.Sampler = None

    # Uniform buffers
    blur_ubo: wgpu.Buffer = None
    comp_ubo: wgpu.Buffer = None

    # Bind groups (two for ping-pong, share same uniform buffers)
    bg_from_a: wgpu.BindGroup = None
    bg_from_b: wgpu.BindGroup = None

    # Tunables
    downsample: int = 2
    iterations: int = 3
    radius_px: float = 6.0
    alpha: float = 1.0

    color_format = wgpu.TextureFormat.BGRA8_UNORM

    def _create(self):
        super()._create()
        self.create_offscreen_targets()   # depends on viewport size
        self.create_pipelines_and_bindings()

    # If your framework has a resize hook, call create_offscreen_targets() there.
    # Otherwise, we can lazily detect size changes in _draw() and rebuild.

    def _current_offscreen_size(self) -> tuple[int, int]:
        vp = Viewport.get_current()
        w = vp.width
        h = vp.height
        #w = max(1, w // self.downsample)
        #h = max(1, h // self.downsample)
        return w, h

    def create_offscreen_targets(self):
        w, h = self._current_offscreen_size()

        usage = (
            wgpu.TextureUsage.RENDER_ATTACHMENT
            | wgpu.TextureUsage.TEXTURE_BINDING
            | wgpu.TextureUsage.COPY_SRC
            | wgpu.TextureUsage.COPY_DST
        )

        desc_offscreen_a = wgpu.TextureDescriptor(
            label="Blur Offscreen A",
            size=wgpu.Extent3D(width=w, height=h, depth_or_array_layers=1),
            mip_level_count=1,
            sample_count=1,
            dimension=wgpu.TextureDimension.E2D,
            format=self.color_format,
            usage=usage,
        )
        desc_offscreen_b = wgpu.TextureDescriptor(
            label="Blur Offscreen B",
            size=wgpu.Extent3D(width=w, height=h, depth_or_array_layers=1),
            mip_level_count=1,
            sample_count=1,
            dimension=wgpu.TextureDimension.E2D,
            format=self.color_format,
            usage=usage,
        )
        self.off_tex_a = self.device.create_texture(desc_offscreen_a)
        self.off_tex_b = self.device.create_texture(desc_offscreen_b)

        self.off_view_a = self.off_tex_a.create_view()
        self.off_view_b = self.off_tex_b.create_view()

        logger.info(f"Offscreen targets: {w}x{h} (downsample={self.downsample})")

    def create_pipelines_and_bindings(self):
        shader = self.gfx.create_shader_module(WGSL)

        # --- Scene pipeline (renders triangle to offscreen) -----------------------
        vertAttributes = [
            wgpu.VertexAttribute(format=wgpu.VertexFormat.FLOAT32X4, offset=0, shader_location=0),
            wgpu.VertexAttribute(format=wgpu.VertexFormat.FLOAT32X4, offset=4 * sizeof(c_float), shader_location=1),
        ]
        vb_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=8 * sizeof(c_float),
                attributes=vertAttributes,
            )
        ]

        scene_fragment = wgpu.FragmentState(
            module=shader,
            entry_point="fs_scene",
            targets=[wgpu.ColorTargetState(format=self.color_format)],
        )
        scene_vertex = wgpu.VertexState(
            module=shader,
            entry_point="vs_scene",
            buffers=vb_layouts,
        )
        self.scene_pipeline = self.device.create_render_pipeline(
            wgpu.RenderPipelineDescriptor(
                label="Scene->Offscreen Pipeline",
                vertex=scene_vertex,
                fragment=scene_fragment,
                primitive=wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_LIST),
            )
        )

        # --- Shared sampler ------------------------------------------------------
        self.sampler = self.device.create_sampler(
            wgpu.SamplerDescriptor(
                label="Blur Sampler",
                address_mode_u=wgpu.AddressMode.CLAMP_TO_EDGE,
                address_mode_v=wgpu.AddressMode.CLAMP_TO_EDGE,
                min_filter=wgpu.FilterMode.LINEAR,
                mag_filter=wgpu.FilterMode.LINEAR,
                mipmap_filter=wgpu.MipmapFilterMode.NEAREST,
            )
        )

        # --- Uniform buffers (COPY_DST so we can write each pass) -----------------
        self.blur_ubo = self.device.create_buffer(
            wgpu.BufferDescriptor(
                label="Blur UBO",
                size=32,
                usage=wgpu.BufferUsage.UNIFORM | wgpu.BufferUsage.COPY_DST,
                mapped_at_creation=False,
            )
        )
        self.comp_ubo = self.device.create_buffer(
            wgpu.BufferDescriptor(
                label="Composite UBO",
                size=32,
                usage=wgpu.BufferUsage.UNIFORM | wgpu.BufferUsage.COPY_DST,
                mapped_at_creation=False,
            )
        )

        # --- Bind group layout ---------------------------------------------------
        # bindings:
        # 0: texture
        # 1: sampler
        # 2: BlurParams uniform
        # 3: CompositeParams uniform  (only used by composite pipeline, but harmless to share)
        self.blur_bgl = self.device.create_bind_group_layout(
            wgpu.BindGroupLayoutDescriptor(
                label="Blur BGL",
                entries=[
                    wgpu.BindGroupLayoutEntry(
                        binding=0,
                        visibility=wgpu.ShaderStage.FRAGMENT,
                        texture=wgpu.TextureBindingLayout(
                            sample_type=wgpu.TextureSampleType.FLOAT,
                            view_dimension=wgpu.TextureViewDimension.E2D,
                            multisampled=False,
                        ),
                    ),
                    wgpu.BindGroupLayoutEntry(
                        binding=1,
                        visibility=wgpu.ShaderStage.FRAGMENT,
                        sampler=wgpu.SamplerBindingLayout(type=wgpu.SamplerBindingType.FILTERING),
                    ),
                    wgpu.BindGroupLayoutEntry(
                        binding=2,
                        visibility=wgpu.ShaderStage.FRAGMENT,
                        buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
                    ),
                    wgpu.BindGroupLayoutEntry(
                        binding=3,
                        visibility=wgpu.ShaderStage.FRAGMENT,
                        buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
                    ),
                ],
            )
        )
        self.blur_pl = self.device.create_pipeline_layout(
            wgpu.PipelineLayoutDescriptor(label="Blur Pipeline Layout", bind_group_layouts=[self.blur_bgl])
        )

        # --- Blur pipeline (fullscreen triangle, no vertex buffers) --------------
        blur_fragment = wgpu.FragmentState(
            module=shader,
            entry_point="fs_kawase",
            targets=[wgpu.ColorTargetState(format=self.color_format)],
        )
        blur_vertex = wgpu.VertexState(module=shader, entry_point="vs_fullscreen", buffers=[])
        self.blur_pipeline = self.device.create_render_pipeline(
            wgpu.RenderPipelineDescriptor(
                label="Kawase Blur Pipeline",
                layout=self.blur_pl,
                vertex=blur_vertex,
                fragment=blur_fragment,
                primitive=wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_LIST),
            )
        )

        # --- Composite pipeline (fullscreen triangle + blend onto swapchain) -----
        # Premultiplied "over" blend:
        blend = wgpu.BlendState(
            color=wgpu.BlendComponent(
                operation=wgpu.BlendOperation.ADD,
                src_factor=wgpu.BlendFactor.ONE,
                dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
            ),
            alpha=wgpu.BlendComponent(
                operation=wgpu.BlendOperation.ADD,
                src_factor=wgpu.BlendFactor.ONE,
                dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
            ),
        )

        comp_fragment = wgpu.FragmentState(
            module=shader,
            entry_point="fs_composite",
            targets=[wgpu.ColorTargetState(format=self.color_format, blend=blend)],
        )
        comp_vertex = wgpu.VertexState(module=shader, entry_point="vs_fullscreen", buffers=[])
        self.composite_pipeline = self.device.create_render_pipeline(
            wgpu.RenderPipelineDescriptor(
                label="Composite Pipeline",
                layout=self.blur_pl,
                vertex=comp_vertex,
                fragment=comp_fragment,
                primitive=wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_LIST),
            )
        )

        # --- Bind groups (two: sampling from A vs sampling from B) ---------------
        def make_bg(view: wgpu.TextureView, label: str) -> wgpu.BindGroup:
            return self.device.create_bind_group(
                wgpu.BindGroupDescriptor(
                    label=label,
                    layout=self.blur_bgl,
                    entries=[
                        wgpu.BindGroupEntry(binding=0, texture_view=view),
                        wgpu.BindGroupEntry(binding=1, sampler=self.sampler),
                        wgpu.BindGroupEntry(binding=2, buffer=self.blur_ubo),
                        wgpu.BindGroupEntry(binding=3, buffer=self.comp_ubo),
                    ],
                )
            )

        self.bg_from_a = make_bg(self.off_view_a, "BG from Offscreen A")
        self.bg_from_b = make_bg(self.off_view_b, "BG from Offscreen B")

    def _write_blur_uniforms(self, tex_w: int, tex_h: int, offset_px: float):
        params = BlurParamsCPU(
            texel_size_x=1.0 / float(tex_w),
            texel_size_y=1.0 / float(tex_h),
            offset=offset_px,
        )
        self.queue.write_buffer(self.blur_ubo, 0, params.to_bytes())

    def _write_composite_uniforms(self):
        params = CompositeParamsCPU(alpha=float(self.alpha))
        self.queue.write_buffer(self.comp_ubo, 0, params.to_bytes())

    def _draw_scene_to_offscreen(self, encoder: wgpu.CommandEncoder):
        # Render the demo triangle into offscreen A
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=self.off_view_a,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 0),
            )
        ]
        rp_desc = wgpu.RenderPassDescriptor(label="Capture Scene Pass", color_attachments=color_attachments)
        pass_enc = encoder.begin_render_pass(rp_desc)
        pass_enc.set_pipeline(self.scene_pipeline)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32)
        pass_enc.draw_indexed(3)
        pass_enc.end()

    def _blur_ping_pong(self, encoder: wgpu.CommandEncoder):
        # Ping-pong between A and B for N iterations.
        tex_w = self.off_tex_a.get_width()
        tex_h = self.off_tex_a.get_height()

        def blur_pass(src_is_a: bool, dst_view: wgpu.TextureView, offset_px: float, label: str):
            self._write_blur_uniforms(tex_w, tex_h, offset_px)

            ca = [
                wgpu.RenderPassColorAttachment(
                    view=dst_view,
                    load_op=wgpu.LoadOp.CLEAR,
                    store_op=wgpu.StoreOp.STORE,
                    clear_value=wgpu.Color(0, 0, 0, 0),
                )
            ]
            rp = encoder.begin_render_pass(wgpu.RenderPassDescriptor(label=label, color_attachments=ca))
            rp.set_pipeline(self.blur_pipeline)
            rp.set_bind_group(0, self.bg_from_a if src_is_a else self.bg_from_b)
            rp.draw(3, 1, 0, 0)  # fullscreen triangle
            rp.end()

        offset = 1.0
        for i in range(self.iterations):
            blur_pass(True, self.off_view_b, offset, f"Blur Pass {i} A->B")
            blur_pass(False, self.off_view_a, offset, f"Blur Pass {i} B->A")
            offset += 1.0

    def _composite_to_viewport(self, encoder: wgpu.CommandEncoder):
        viewport = Viewport.get_current()

        self._write_composite_uniforms()

        ca = [
            wgpu.RenderPassColorAttachment(
                view=viewport.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]
        rp = encoder.begin_render_pass(wgpu.RenderPassDescriptor(label="Composite Pass", color_attachments=ca))
        rp.set_pipeline(self.composite_pipeline)
        # final blurred result is in A
        rp.set_bind_group(0, self.bg_from_a)
        rp.draw(3, 1, 0, 0)
        rp.end()

    def _draw(self):
        # If you can detect viewport resize, rebuild offscreen + bind groups here.
        # Minimal prototype: assume fixed size.

        #encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        encoder: wgpu.CommandEncoder = Renderer.get_current().encoder

        self._draw_scene_to_offscreen(encoder)
        self._blur_ping_pong(encoder)
        self._composite_to_viewport(encoder)

        #self.queue.submit([encoder.finish()])
        super()._draw()
