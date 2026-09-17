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

  // Unit quad centered on the origin (-0.5..0.5), same as the old vertex data
  let pos = vec4<f32>(corner - vec2<f32>(0.5), 0.0, 1.0);

  // Corner doubles as the UV; flip v so image row 0 lands at the top
  let uv = vec2<f32>(corner.x, 1.0 - corner.y);

  return VertexOutput(uniforms.modelViewProjectionMatrix * pos, uv);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  return textureSample(myTexture, mySampler, in.uv);
}
"""


class SpriteShaderDemo(Demo):
    texture: wgpu.Texture = None
    sampler: wgpu.Sampler = None

    def create_device_objects(self):
        self.create_buffers()
        self.create_textures()
        self.create_pipeline()

    def create_pipeline(self):
        shader_module = self.gfx.create_shader_module(shader_code)

        color_targets = [
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
            )
        ]

        fragmentState = wgpu.FragmentState(
            module=shader_module,
            entry_point="fs_main",
            targets=color_targets,
        )

        # No vertex buffers: positions and UVs come from vertex_index
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

        bgl_desc = wgpu.BindGroupLayoutDescriptor(entries=bgl_entries)

        bgl = self.device.create_bind_group_layout(bgl_desc)

        pl_desc = wgpu.PipelineLayoutDescriptor(bind_group_layouts=[bgl])

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            primitive=primitive,
            fragment=fragmentState,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

        view: wgpu.TextureView = self.texture.create_view()

        bindgroup_entries = [
            wgpu.BindGroupEntry(binding=0, sampler=self.sampler),
            wgpu.BindGroupEntry(binding=1, texture_view=view),
            wgpu.BindGroupEntry(
                binding=2, buffer=self.uniformBuffer, size=self.uniformBufferSize
            ),
        ]

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Texture bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entries=bindgroup_entries,
        )

        self.bindGroup = self.device.create_bind_group(bindGroupDesc)
        logger.debug(self.bindGroup)

    def create_buffers(self):
        self.uniformBufferSize = 4 * 16
        self.uniformBuffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            self.uniformBufferSize,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_textures(self):
        path = self.resource_root / "images" / "playerShip1_orange.png"
        im = iio.imread(path)
        shape = im.shape
        logger.debug(shape)
        im_height, im_width, im_channels = shape
        im_depth = 1

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        self.texture = self.device.create_texture(descriptor)

        self.sampler = self.device.create_sampler()

        bytes_per_row = im_channels * im_width
        logger.debug(bytes_per_row)
        rows_per_image = im_height

        self.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.TexelCopyTextureInfo(
                texture=self.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            im,
            # The layout of the texture
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=bytes_per_row,
                rows_per_image=rows_per_image,
            ),
            # The texture size
            wgpu.Extent3D(im_width, im_height, im_depth),
        )

    def _draw(self):
        viewport = Viewport.get_current()
        easel = viewport.easel

        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=easel.color_texture_view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachments=color_attachments,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bindGroup)
        pass_enc.draw(4)
        pass_enc.end()
        command_buffer = encoder.finish()

        self.queue.submit([command_buffer])

        super()._draw()

    def frame(self):
        viewport = self.viewport
        viewport_width = viewport.width
        viewport_height = viewport.height

        x = viewport_width / 2
        y = viewport_height / 2

        model = glm.mat4(1.0)  # Identity matrix
        model = glm.translate(model, glm.vec3(x, y, 0))
        model = glm.rotate(model, glm.radians(45.0), glm.vec3(0, 0, 1))
        model = glm.scale(model, glm.vec3(200, 200, 1))

        view = glm.mat4(1.0)  # Identity matrix

        ortho_left = 0
        ortho_right = viewport_width
        ortho_bottom = 0
        ortho_top = viewport_height
        ortho_near = -1  # Near clipping plane
        ortho_far = 1  # Far clipping plane

        projection = glm.ortho(
            ortho_left, ortho_right, ortho_bottom, ortho_top, ortho_near, ortho_far
        )

        transform = projection * view * model

        self.device.queue.write_buffer(self.uniformBuffer, 0, transform)

        super().frame()


def main():
    SpriteShaderDemo().run()


if __name__ == "__main__":
    main()