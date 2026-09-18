"""Depth-buffered sprite demo — order independence vs. edge quality.

Draws the same pair of overlapping sprites twice, both submitted in the
WRONG painter's order (near sprite first, far sprite second):

  LEFT    Alpha blending, no depth test. Smooth antialiased edges, but the
          far sprite paints over the near one. Wrong, because blending
          depends entirely on draw order.

  RIGHT   Depth test + depth write, alpha test (discard) instead of
          blending. Correct occlusion despite the identical wrong
          submission order, because each sprite's depth comes from its sort
          key rather than its position in the stream. Look closely at the
          silhouette: the antialiased border pixels are gone, replaced by a
          hard stair-stepped edge. That is what the discard costs.

The depth is written in the vertex shader straight from a uniform, which is
the technique itself in miniature: whatever you would have sorted by becomes
the z, and the depth buffer does the sorting for you.

Flip SUBMIT_IN_SORTED_ORDER to True to confirm the left half is only wrong
because of the order — it goes correct, and the right half doesn't change.
"""

from ctypes import c_float, sizeof

from loguru import logger
import numpy as np
import imageio.v3 as iio
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.engine import Viewport

from ..demo import Demo


# Submitting near-then-far violates the painter's algorithm on purpose. Set
# this True to submit far-then-near and watch only the left half change.
SUBMIT_IN_SORTED_ORDER = False

# Texel alpha at or above this survives the discard. 0.5 is the usual
# starting point; raise it to shrink the silhouette, lower it to grow a
# fringe of half-transparent pixels that now read as fully opaque.
ALPHA_CUTOFF = 0.5

SPRITE_SCALE = 300.0
SPRITE_OFFSET = 55.0

# Uniform buffer offsets must be 256-byte aligned, so each sprite gets a
# 256-byte slot even though the struct itself is 80.
UNIFORM_SIZE = 80
SLOT_STRIDE = 256

# Slot order is also submission order.
SLOT_LEFT_NEAR = 0
SLOT_LEFT_FAR = 1
SLOT_RIGHT_NEAR = 2
SLOT_RIGHT_FAR = 3
SLOT_COUNT = 4

# NDC depth, 0 near .. 1 far, compared with LESS.
DEPTH_NEAR = 0.3
DEPTH_FAR = 0.6

# ASSUMPTION: DEPTH24_PLUS is the crunge.wgpu spelling of wgpu::TextureFormat::Depth24Plus.
DEPTH_FORMAT = wgpu.TextureFormat.DEPTH24_PLUS


shader_code = """
@group(0) @binding(0) var mySampler: sampler;
@group(0) @binding(1) var myTexture : texture_2d<f32>;

struct Uniforms {
  modelViewProjectionMatrix : mat4x4<f32>,
  depth : f32,
  alpha_cutoff : f32,
  use_alpha_test : f32,
  _pad : f32,
}
@group(0) @binding(2) var<uniform> uniforms : Uniforms;

struct VertexInput {
  @location(0) pos: vec2<f32>,
  @location(1) uv: vec2<f32>,
}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
}

@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
  var vert_pos = uniforms.modelViewProjectionMatrix * vec4<f32>(in.pos, 0.0, 1.0);

  // The whole trick, one line. The projection's own z is discarded and
  // replaced by the sort key. Safe to assign NDC z directly because an
  // orthographic transform leaves w at 1, so there is no perspective divide
  // to undo. WebGPU clips z to [0, 1], unlike OpenGL's [-1, 1].
  vert_pos.z = uniforms.depth;

  return VertexOutput(vert_pos, in.uv);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  let uv = vec2<f32>(in.uv.x, 1.0 - in.uv.y);
  let color = textureSample(myTexture, mySampler, uv);

  // Sampling happens before the discard on purpose: texture sampling needs
  // uniform control flow for its derivatives, so discarding first would be
  // a validation error.
  if (uniforms.use_alpha_test > 0.5 && color.a < uniforms.alpha_cutoff) {
    discard;
  }

  return color;
}
"""

index_data = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint32)

vertex_data = np.array(
    [
        -0.5, 0.5, 0.0, 1.0,   # top-left
        -0.5, -0.5, 0.0, 0.0,  # bottom-left
        0.5, -0.5, 1.0, 0.0,   # bottom-right
        0.5, 0.5, 1.0, 1.0,    # top-right
    ],
    dtype=np.float32,
)


class SpriteDepthDemo(Demo):
    vertex_buffer: wgpu.Buffer = None
    index_buffer: wgpu.Buffer = None

    texture: wgpu.Texture = None
    sampler: wgpu.Sampler = None

    depth_texture: wgpu.Texture = None
    depth_texture_view: wgpu.TextureView = None

    # Blending, no depth test — the conventional sorted path.
    blend_pipeline: wgpu.RenderPipeline = None
    # Depth test and write, alpha test, no blending.
    depth_pipeline: wgpu.RenderPipeline = None

    def __init__(self) -> None:
        super().__init__()
        self.depth_size = (0, 0)
        self.bind_groups: list[wgpu.BindGroup] = []

    def create_device_objects(self):
        self.create_buffers()
        self.create_textures()
        self.ensure_depth_texture(self.viewport.width, self.viewport.height)
        self.create_pipelines()
        self.create_bind_groups()

    # -- resources ---------------------------------------------------------

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer_from_ndarray(
            self.device, "INDEX", index_data, wgpu.BufferUsage.INDEX
        )
        self.uniform_buffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            SLOT_STRIDE * SLOT_COUNT,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_textures(self):
        path = self.resource_root / "images" / "playerShip1_orange.png"
        im = iio.imread(path)
        im_height, im_width, im_channels = im.shape
        im_depth = 1
        logger.debug(f"sprite texture: {im.shape}")

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )
        self.texture = self.device.create_texture(descriptor)

        # The original demo took the default sampler, which is NEAREST. At
        # this magnification that would give the blended half blocky edges
        # too, and the comparison would show nothing.
        self.sampler = self.device.create_sampler(
            wgpu.SamplerDescriptor(
                label="Linear Sampler",
                mag_filter=wgpu.FilterMode.LINEAR,
                min_filter=wgpu.FilterMode.LINEAR,
                address_mode_u=wgpu.AddressMode.CLAMP_TO_EDGE,
                address_mode_v=wgpu.AddressMode.CLAMP_TO_EDGE,
            )
        )

        self.queue.write_texture(
            wgpu.TexelCopyTextureInfo(
                texture=self.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            im,
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=im_channels * im_width,
                rows_per_image=im_height,
            ),
            wgpu.Extent3D(im_width, im_height, im_depth),
        )

    def ensure_depth_texture(self, width: int, height: int):
        """The depth target has to track the colour target's size."""
        if (width, height) == self.depth_size:
            return
        if width <= 0 or height <= 0:
            return

        logger.debug(f"creating depth texture: {width}x{height}")
        self.depth_texture = self.device.create_texture(
            wgpu.TextureDescriptor(
                label="Depth Texture",
                dimension=wgpu.TextureDimension.E2D,
                size=wgpu.Extent3D(width, height, 1),
                sample_count=1,
                format=DEPTH_FORMAT,
                mip_level_count=1,
                usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            )
        )
        self.depth_texture_view = self.depth_texture.create_view()
        self.depth_size = (width, height)

    # -- pipelines ---------------------------------------------------------

    def create_pipelines(self):
        shader_module = self.gfx.create_shader_module(shader_code)

        vert_attributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2, offset=0, shader_location=0
            ),
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X2,
                offset=2 * sizeof(c_float),
                shader_location=1,
            ),
        ]

        vb_layouts = [
            wgpu.VertexBufferLayout(
                array_stride=4 * sizeof(c_float),
                attributes=vert_attributes,
            )
        ]

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
            buffers=vb_layouts,
        )

        bgl_entries = [
            wgpu.BindGroupLayoutEntry(
                binding=0,
                visibility=wgpu.ShaderStage.FRAGMENT,
                sampler=wgpu.SamplerBindingLayout(
                    type=wgpu.SamplerBindingType.FILTERING
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=1,
                visibility=wgpu.ShaderStage.FRAGMENT,
                texture=wgpu.TextureBindingLayout(
                    sample_type=wgpu.TextureSampleType.FLOAT,
                    view_dimension=wgpu.TextureViewDimension.E2D,
                ),
            ),
            wgpu.BindGroupLayoutEntry(
                binding=2,
                # Depth lands in the vertex stage, the cutoff in the fragment
                # stage, so this uniform is visible to both.
                visibility=wgpu.ShaderStage.VERTEX | wgpu.ShaderStage.FRAGMENT,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        self.bind_group_layout = self.device.create_bind_group_layout(
            wgpu.BindGroupLayoutDescriptor(entries=bgl_entries)
        )
        pipeline_layout = self.device.create_pipeline_layout(
            wgpu.PipelineLayoutDescriptor(bind_group_layouts=[self.bind_group_layout])
        )

        blend_state = wgpu.BlendState(
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

        # Both pipelines need a depth-stencil state, because the render pass
        # carries a depth attachment and every pipeline used in it has to be
        # compatible with the attachment — even the one that ignores depth.
        # ASSUMPTION: recent Dawn types depthWriteEnabled as OptionalBool. If
        # a plain bool is rejected here, it wants wgpu.OptionalBool.TRUE/FALSE.
        blend_depth_state = wgpu.DepthStencilState(
            format=DEPTH_FORMAT,
            depth_write_enabled=False,
            depth_compare=wgpu.CompareFunction.ALWAYS,
        )
        test_depth_state = wgpu.DepthStencilState(
            format=DEPTH_FORMAT,
            depth_write_enabled=True,
            depth_compare=wgpu.CompareFunction.LESS,
        )

        self.blend_pipeline = self.device.create_render_pipeline(
            wgpu.RenderPipelineDescriptor(
                label="Blended Sprite Pipeline",
                layout=pipeline_layout,
                vertex=vertex_state,
                fragment=wgpu.FragmentState(
                    module=shader_module,
                    entry_point="fs_main",
                    targets=[
                        wgpu.ColorTargetState(
                            format=wgpu.TextureFormat.BGRA8_UNORM,
                            blend=blend_state,
                        )
                    ],
                ),
                depth_stencil=blend_depth_state,
            )
        )

        self.depth_pipeline = self.device.create_render_pipeline(
            wgpu.RenderPipelineDescriptor(
                label="Depth Tested Sprite Pipeline",
                layout=pipeline_layout,
                vertex=vertex_state,
                fragment=wgpu.FragmentState(
                    module=shader_module,
                    entry_point="fs_main",
                    # No blend state. Every surviving fragment is fully
                    # opaque, which is exactly what lets it write depth
                    # honestly — a blended fragment would write depth as if
                    # it were solid and occlude whatever sorts behind it.
                    targets=[
                        wgpu.ColorTargetState(format=wgpu.TextureFormat.BGRA8_UNORM)
                    ],
                ),
                depth_stencil=test_depth_state,
            )
        )

    def create_bind_groups(self):
        view: wgpu.TextureView = self.texture.create_view()
        self.bind_groups = []

        for slot in range(SLOT_COUNT):
            entries = [
                wgpu.BindGroupEntry(binding=0, sampler=self.sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=view),
                wgpu.BindGroupEntry(
                    binding=2,
                    buffer=self.uniform_buffer,
                    offset=slot * SLOT_STRIDE,
                    size=UNIFORM_SIZE,
                ),
            ]
            self.bind_groups.append(
                self.device.create_bind_group(
                    wgpu.BindGroupDescriptor(
                        label=f"Sprite bind group {slot}",
                        layout=self.bind_group_layout,
                        entries=entries,
                    )
                )
            )

    # -- per frame ---------------------------------------------------------

    def write_slot(
        self,
        slot: int,
        transform: glm.mat4,
        depth: float,
        use_alpha_test: bool,
    ):
        base = slot * SLOT_STRIDE
        # The matrix goes in as a glm object, the way the original demo wrote
        # it — avoids any question about numpy's flattening order.
        self.queue.write_buffer(self.uniform_buffer, base, transform)
        params = np.array(
            [depth, ALPHA_CUTOFF, 1.0 if use_alpha_test else 0.0, 0.0],
            dtype=np.float32,
        )
        self.queue.write_buffer(self.uniform_buffer, base + 64, params)

    def frame(self):
        viewport = self.viewport
        width = viewport.width
        height = viewport.height

        self.ensure_depth_texture(width, height)

        projection = glm.ortho(0, width, 0, height, -1, 1)
        view = glm.mat4(1.0)

        def sprite_transform(cx: float, cy: float, dx: float, dy: float, angle: float):
            model = glm.mat4(1.0)
            model = glm.translate(model, glm.vec3(cx + dx, cy + dy, 0))
            model = glm.rotate(model, glm.radians(angle), glm.vec3(0, 0, 1))
            model = glm.scale(model, glm.vec3(SPRITE_SCALE, SPRITE_SCALE, 1))
            return projection * view * model

        left_x, right_x = width * 0.25, width * 0.75
        center_y = height * 0.5

        near = (SPRITE_OFFSET, -SPRITE_OFFSET, -20.0)
        far = (-SPRITE_OFFSET, SPRITE_OFFSET, 20.0)

        self.write_slot(
            SLOT_LEFT_NEAR, sprite_transform(left_x, center_y, *near), DEPTH_NEAR, False
        )
        self.write_slot(
            SLOT_LEFT_FAR, sprite_transform(left_x, center_y, *far), DEPTH_FAR, False
        )
        self.write_slot(
            SLOT_RIGHT_NEAR, sprite_transform(right_x, center_y, *near), DEPTH_NEAR, True
        )
        self.write_slot(
            SLOT_RIGHT_FAR, sprite_transform(right_x, center_y, *far), DEPTH_FAR, True
        )

        super().frame()

    def _draw(self):
        viewport = Viewport.get_current()
        easel = viewport.easel

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=easel.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0.1, 0.1, 0.12, 1),
            )
        ]

        # Cleared to 1.0 — the far plane — so the first fragment at any pixel
        # always passes LESS.
        depth_attachment = wgpu.RenderPassDepthStencilAttachment(
            view=self.depth_texture_view,
            depth_load_op=wgpu.LoadOp.CLEAR,
            depth_store_op=wgpu.StoreOp.STORE,
            depth_clear_value=1.0,
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Depth Demo Render Pass",
            color_attachments=color_attachments,
            depth_stencil_attachment=depth_attachment,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)

        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32)

        if SUBMIT_IN_SORTED_ORDER:
            left = (SLOT_LEFT_FAR, SLOT_LEFT_NEAR)
            right = (SLOT_RIGHT_FAR, SLOT_RIGHT_NEAR)
        else:
            left = (SLOT_LEFT_NEAR, SLOT_LEFT_FAR)
            right = (SLOT_RIGHT_NEAR, SLOT_RIGHT_FAR)

        pass_enc.set_pipeline(self.blend_pipeline)
        for slot in left:
            pass_enc.set_bind_group(0, self.bind_groups[slot])
            pass_enc.draw_indexed(6)

        pass_enc.set_pipeline(self.depth_pipeline)
        for slot in right:
            pass_enc.set_bind_group(0, self.bind_groups[slot])
            pass_enc.draw_indexed(6)

        pass_enc.end()
        self.queue.submit([encoder.finish()])

        super()._draw()


# Notes on what this demo deliberately leaves out
# -----------------------------------------------
#
# Alpha-to-coverage is the usual mitigation for the hard edge on the right.
# With an MSAA colour target, the hardware converts fragment alpha into a
# coverage mask, so a border texel at 40% alpha lights roughly 40% of the
# samples instead of being discarded outright. That buys back most of the
# antialiasing while keeping order independence, at the cost of running the
# pass multisampled. It needs sample_count > 1 on the texture, the pipeline
# multisample state, and a resolve target, which is more machinery than
# belongs in a comparison this small.
#
# The other standard arrangement is two passes: this depth-tested pass for
# everything opaque, then a blended pass for the genuinely translucent
# things, sorted back to front, depth test on but depth write off. The
# second pass gives up batching, but there are usually far fewer of those.

def main():
    SpriteDepthDemo().run()


if __name__ == "__main__":
    main()