from __future__ import annotations

from dataclasses import dataclass
import numpy as np

from crunge import wgpu

from .base import Base


# WGSL with support for both premultiplied and non-premultiplied sources
WGSL_COMPOSITOR = r"""
struct VSOut {
  @builtin(position) pos: vec4f,
  @location(0) uv: vec2f,
};

@vertex
fn vs_fullscreen(@builtin(vertex_index) vid: u32) -> VSOut {
  var p = array<vec2f, 3>(
    vec2f(-1.0, -1.0),
    vec2f( 3.0, -1.0),
    vec2f(-1.0,  3.0)
  );
  let pos = p[vid];

  var o: VSOut;
  o.pos = vec4f(pos, 0.0, 1.0);

  // clip -> uv, flip Y
  let uv0 = 0.5 * (pos + vec2f(1.0, 1.0));
  o.uv = vec2f(uv0.x, 1.0 - uv0.y);
  return o;
}

@group(0) @binding(0) var src_tex: texture_2d<f32>;
@group(0) @binding(1) var src_samp: sampler;

struct Params {
  alpha: f32,
  is_premultiplied: f32,  // 1.0 if source is already premultiplied, 0.0 otherwise
  _pad0: vec2f,
};
@group(0) @binding(2) var<uniform> u: Params;

@fragment
fn fs_composite(in: VSOut) -> @location(0) vec4f {
  let c = textureSample(src_tex, src_samp, in.uv);
  let a = u.alpha;

  // If source is already premultiplied, just scale by alpha
  // Otherwise, premultiply it
  if (u.is_premultiplied > 0.5) {
    // Source is premultiplied - just apply alpha scale
    return vec4f(c.rgb * a, c.a * a);
  } else {
    // Source is NOT premultiplied - premultiply for correct "over" blending
    let out_a = c.a * a;
    return vec4f(c.rgb * out_a, out_a);
  }
}
"""


@dataclass
class CompositeParamsCPU:
    alpha: float
    is_premultiplied: float = 0.0  # 0.0 = non-premultiplied, 1.0 = premultiplied
    _pad0: float = 0.0
    _pad1: float = 0.0

    def to_bytes(self) -> bytes:
        return np.array([self.alpha, self.is_premultiplied, self._pad0, self._pad1], dtype=np.float32).tobytes()


class Compositor(Base):
    """
    Composite a source viewport color texture onto a destination viewport color attachment
    using a fullscreen triangle.

    - src: texture_2d<f32> + sampler
    - dst: RenderPassColorAttachment view
    - optional alpha
    - premultiplied "over" blending enabled by default
    - supports both premultiplied and non-premultiplied sources
    """

    def __init__(
        self,
        color_format: wgpu.TextureFormat = wgpu.TextureFormat.BGRA8_UNORM,
        enable_blend: bool = True,
    ):
        super().__init__()

        self.color_format = color_format
        self.enable_blend = enable_blend

        self.shader = self.gfx.create_shader_module(WGSL_COMPOSITOR)

        self.sampler = self.device.create_sampler(
            wgpu.SamplerDescriptor(
                label="Compositor Sampler",
                address_mode_u=wgpu.AddressMode.CLAMP_TO_EDGE,
                address_mode_v=wgpu.AddressMode.CLAMP_TO_EDGE,
                min_filter=wgpu.FilterMode.LINEAR,
                mag_filter=wgpu.FilterMode.LINEAR,
                mipmap_filter=wgpu.MipmapFilterMode.NEAREST,
            )
        )

        self.ubo = self.device.create_buffer(
            wgpu.BufferDescriptor(
                label="Compositor UBO",
                size=32,
                usage=wgpu.BufferUsage.UNIFORM | wgpu.BufferUsage.COPY_DST,
                mapped_at_creation=False,
            )
        )

        # BGL: 0 texture, 1 sampler, 2 uniform
        self.bgl = self.device.create_bind_group_layout(
            wgpu.BindGroupLayoutDescriptor(
                label="Compositor BGL",
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
                ],
            )
        )
        self.pl = self.device.create_pipeline_layout(
            wgpu.PipelineLayoutDescriptor(label="Compositor PL", bind_group_layouts=[self.bgl])
        )

        blend = None
        if self.enable_blend:
            # Premultiplied "over"
            blend = wgpu.BlendState(
                color=wgpu.BlendComponent(
                    operation=wgpu.BlendOperation.ADD,
                    src_factor=wgpu.BlendFactor.SRC_ALPHA,
                    dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
                ),
                alpha=wgpu.BlendComponent(
                    operation=wgpu.BlendOperation.ADD,
                    src_factor=wgpu.BlendFactor.ONE,
                    dst_factor=wgpu.BlendFactor.ONE_MINUS_SRC_ALPHA,
                ),
            )

        fragment = wgpu.FragmentState(
            module=self.shader,
            entry_point="fs_composite",
            targets=[wgpu.ColorTargetState(format=self.color_format, blend=blend)],
        )
        vertex = wgpu.VertexState(module=self.shader, entry_point="vs_fullscreen", buffers=[])

        self.pipeline = self.device.create_render_pipeline(
            wgpu.RenderPipelineDescriptor(
                label="Compositor Pipeline",
                layout=self.pl,
                vertex=vertex,
                fragment=fragment,
                primitive=wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_LIST),
            )
        )

        # Cache bind groups per TextureView id() (views are usually stable per viewport)
        self._bg_cache: dict[int, wgpu.BindGroup] = {}

    def _write_uniforms(self, alpha: float, is_premultiplied: bool = False) -> None:
        params = CompositeParamsCPU(
            alpha=float(alpha),
            is_premultiplied=1.0 if is_premultiplied else 0.0
        )
        self.queue.write_buffer(self.ubo, 0, params.to_bytes())

    def _bind_group_for_view(self, src_view: wgpu.TextureView) -> wgpu.BindGroup:
        key = id(src_view)
        bg = self._bg_cache.get(key)
        if bg is not None:
            return bg

        bg = self.device.create_bind_group(
            wgpu.BindGroupDescriptor(
                label="Compositor BG",
                layout=self.bgl,
                entries=[
                    wgpu.BindGroupEntry(binding=0, texture_view=src_view),
                    wgpu.BindGroupEntry(binding=1, sampler=self.sampler),
                    wgpu.BindGroupEntry(binding=2, buffer=self.ubo),
                ],
            )
        )
        self._bg_cache[key] = bg
        return bg

    def composite(
        self,
        encoder: wgpu.CommandEncoder,
        *,
        src_view: wgpu.TextureView,
        dst_view: wgpu.TextureView,
        alpha: float = 1.0,
        is_premultiplied: bool = False,  # NEW: Tell compositor if source is premultiplied
        clear_dst: bool = False,
        clear_value: wgpu.Color = wgpu.Color(0, 0, 0, 0),
        label: str = "Compositor Pass",
    ) -> None:
        """
        Draw src_view onto dst_view.
        
        Args:
            encoder: Command encoder
            src_view: Source texture view to composite
            dst_view: Destination texture view
            alpha: Overall alpha multiplier (0.0-1.0)
            is_premultiplied: True if source is already premultiplied alpha, False otherwise
            clear_dst: Whether to clear destination before compositing
            clear_value: Clear color if clear_dst is True
            label: Debug label for the render pass
            
        If clear_dst=False and blending is enabled, you get "over" compositing.
        If clear_dst=True, you basically do a copy-with-shader (still filtered).
        """
        self._write_uniforms(alpha, is_premultiplied)
        bg = self._bind_group_for_view(src_view)

        ca = [
            wgpu.RenderPassColorAttachment(
                view=dst_view,
                load_op=wgpu.LoadOp.CLEAR if clear_dst else wgpu.LoadOp.LOAD,
                store_op=wgpu.StoreOp.STORE,
                clear_value=clear_value,
            )
        ]
        rp = encoder.begin_render_pass(wgpu.RenderPassDescriptor(label=label, color_attachments=ca))
        rp.set_pipeline(self.pipeline)
        rp.set_bind_group(0, bg)
        rp.draw(3, 1, 0, 0)
        rp.end()