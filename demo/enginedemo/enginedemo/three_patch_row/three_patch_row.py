import math
import time

from loguru import logger
import imageio.v3 as iio
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.engine import Viewport

from ..demo import Demo


shader_code = """
@group(0) @binding(0) var mySampler: sampler;
@group(0) @binding(1) var myTexture : texture_2d<f32>;

struct Uniforms {
  modelViewProjectionMatrix : mat4x4<f32>,
}
@group(0) @binding(2) var<uniform> uniforms : Uniforms;

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) uv: vec2<f32>,
}

@vertex
fn vs_main(@builtin(vertex_index) idx : u32) -> VertexOutput {
  // Triangle strip corners in 0..1 space:
  //   0 = (0,0) bottom-left
  //   1 = (1,0) bottom-right
  //   2 = (0,1) top-left
  //   3 = (1,1) top-right
  let corner = vec2<f32>(f32(idx & 1u), f32((idx >> 1u) & 1u));

  // Quad anchored at its bottom-left corner, so the model matrix is just
  // translate(x, y) * scale(width, height) and patches line up edge to edge.
  let pos = uniforms.modelViewProjectionMatrix * vec4<f32>(corner, 0.0, 1.0);

  // Flip v so image row 0 lands at the top
  let uv = vec2<f32>(corner.x, 1.0 - corner.y);

  return VertexOutput(pos, uv);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  return textureSample(myTexture, mySampler, in.uv);
}
"""


class Patch:
    """One quad of the three patch: its texture, native size, and GPU bindings."""

    def __init__(self, texture: wgpu.Texture, width: int, height: int):
        self.texture = texture
        self.width = width
        self.height = height
        self.uniform_buffer: wgpu.Buffer = None
        self.bind_group: wgpu.BindGroup = None


class ThreePatchRowDemo(Demo):
    image_names = [
        "SpeechBubble_01.png",  # left cap
        "SpeechBubble_02.png",  # stretchable middle
        "SpeechBubble_03.png",  # right cap
    ]

    uniform_buffer_size = 4 * 16

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.patches: list[Patch] = []
        self.sampler: wgpu.Sampler = None
        self.bind_group_layout: wgpu.BindGroupLayout = None
        self.start_time = time.perf_counter()

    def create_device_objects(self):
        self.create_textures()
        self.create_buffers()
        self.create_pipeline()
        self.create_bind_groups()

    def create_textures(self):
        self.sampler = self.device.create_sampler()
        for name in self.image_names:
            path = self.resource_root / "skins" / name
            self.patches.append(self.load_patch(path))

    def load_patch(self, path) -> Patch:
        # Force RGBA so palette or RGB PNGs still match the texture format
        im = iio.imread(path, mode="RGBA")
        im_height, im_width, im_channels = im.shape
        logger.debug(f"{path.name}: {im.shape}")

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, 1),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        texture = self.device.create_texture(descriptor)

        self.queue.write_texture(
            wgpu.TexelCopyTextureInfo(
                texture=texture,
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
            wgpu.Extent3D(im_width, im_height, 1),
        )

        return Patch(texture, im_width, im_height)

    def create_buffers(self):
        for i, patch in enumerate(self.patches):
            patch.uniform_buffer = utils.create_buffer(
                self.device,
                f"Patch {i} uniform buffer",
                self.uniform_buffer_size,
                wgpu.BufferUsage.UNIFORM,
            )

    def create_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

        # Straight (non-premultiplied) alpha blending for the PNG transparency
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

        color_targets = [
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
                blend=blend_state,
            )
        ]

        fragment_state = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=shader_module,
            entry_point="vs_main",
        )

        primitive = wgpu.PrimitiveState(topology=wgpu.PrimitiveTopology.TRIANGLE_STRIP)

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
                visibility=wgpu.ShaderStage.VERTEX,
                buffer=wgpu.BufferBindingLayout(type=wgpu.BufferBindingType.UNIFORM),
            ),
        ]

        # Explicit layout shared by all three patch bind groups
        self.bind_group_layout = self.device.create_bind_group_layout(
            wgpu.BindGroupLayoutDescriptor(entries=bgl_entries)
        )

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layouts=[self.bind_group_layout]
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Three Patch Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive,
            fragment=fragment_state,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

    def create_bind_groups(self):
        for i, patch in enumerate(self.patches):
            entries = [
                wgpu.BindGroupEntry(binding=0, sampler=self.sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=patch.texture.create_view()),
                wgpu.BindGroupEntry(
                    binding=2,
                    buffer=patch.uniform_buffer,
                    size=self.uniform_buffer_size,
                ),
            ]

            patch.bind_group = self.device.create_bind_group(
                wgpu.BindGroupDescriptor(
                    label=f"Patch {i} bind group",
                    layout=self.bind_group_layout,
                    entries=entries,
                )
            )

    def layout_patches(self, x: float, y: float, width: float, height: float):
        """Return (x, width) for each patch: caps keep aspect ratio, middle stretches."""
        left, middle, right = self.patches

        left_width = left.width * (height / left.height)
        right_width = right.width * (height / right.height)
        middle_width = max(width - left_width - right_width, 0.0)

        return [
            (x, left_width),
            (x + left_width, middle_width),
            (x + left_width + middle_width, right_width),
        ]

    def _draw(self):
        viewport = Viewport.get_current()
        easel = viewport.easel

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=easel.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0.2, 0.3, 0.4, 1),
            )
        ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        for patch in self.patches:
            pass_enc.set_bind_group(0, patch.bind_group)
            pass_enc.draw(4)
        pass_enc.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])

        super()._draw()

    def frame(self):
        viewport = self.viewport
        viewport_width = viewport.width
        viewport_height = viewport.height

        projection = glm.ortho(0, viewport_width, 0, viewport_height, -1, 1)
        view = glm.mat4(1.0)

        # Animate the width so the middle patch visibly stretches and shrinks
        elapsed = time.perf_counter() - self.start_time
        bubble_height = 100.0
        bubble_width = viewport_width * (0.5 + 0.25 * math.sin(elapsed))

        bubble_x = (viewport_width - bubble_width) / 2
        bubble_y = (viewport_height - bubble_height) / 2

        placements = self.layout_patches(
            bubble_x, bubble_y, bubble_width, bubble_height
        )

        for patch, (patch_x, patch_width) in zip(self.patches, placements):
            model = glm.translate(glm.mat4(1.0), glm.vec3(patch_x, bubble_y, 0))
            model = glm.scale(model, glm.vec3(patch_width, bubble_height, 1))

            transform = projection * view * model
            self.device.queue.write_buffer(patch.uniform_buffer, 0, transform)

        super().frame()


def main():
    ThreePatchRowDemo().run()


if __name__ == "__main__":
    main()