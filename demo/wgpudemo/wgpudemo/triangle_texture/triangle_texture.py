from ctypes import c_float, sizeof

from loguru import logger
import numpy as np

from crunge import wgpu
import crunge.wgpu.utils as utils

from ..common import Demo, Renderer

vs_shader_code = """
@vertex fn main(@location(0) pos : vec4<f32>) -> @builtin(position) vec4<f32> {
    return pos;
}
"""

fs_shader_code = """
@group(0) @binding(0) var mySampler: sampler;
@group(0) @binding(1) var myTexture : texture_2d<f32>;

@fragment fn main(@builtin(position) FragCoord : vec4<f32>)
                        -> @location(0) vec4<f32> {
    return textureSample(myTexture, mySampler, FragCoord.xy / vec2<f32>(800.0, 600.0));
    //return textureSample(myTexture, mySampler, FragCoord.xy);
}
"""

index_data = np.array([0, 1, 2], dtype=np.uint32)

vertex_data = np.array(
    [
        0.0,
        0.5,
        0.0,
        1.0,
        1.0,
        0.0,
        0.0,
        1.0,
        -0.5,
        -0.5,
        0.0,
        1.0,
        0.0,
        1.0,
        0.0,
        1.0,
        0.5,
        -0.5,
        0.0,
        1.0,
        0.0,
        0.0,
        1.0,
        1.0,
    ],
    dtype=np.float32,
)


class TriangleTextureDemo(Demo):
    vertex_buffer: wgpu.Buffer = None
    index_buffer: wgpu.Buffer = None

    texture: wgpu.Texture = None
    sampler: wgpu.Sampler = None

    kWidth = 800
    kHeight = 600

    def __init__(self):
        super().__init__()

    def create_device_objects(self):
        self.create_buffers()
        self.create_textures()
        self.create_pipeline()

    def create_pipeline(self):
        vs_module = self.create_shader_module(vs_shader_code)
        fs_module = self.create_shader_module(fs_shader_code)

        vertAttributes = [
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X4, offset=0, shader_location=0
            ),
            wgpu.VertexAttribute(
                format=wgpu.VertexFormat.FLOAT32X4,
                offset=4 * sizeof(c_float),
                shader_location=1,
            ),
        ]

        vertBufferLayouts = [
            wgpu.VertexBufferLayout(
                array_stride=8 * sizeof(c_float),
                attribute_count=2,
                attributes=vertAttributes,
            )
        ]

        color_targets = [
            wgpu.ColorTargetState(
                format=wgpu.TextureFormat.BGRA8_UNORM,
            )
        ]

        fragmentState = wgpu.FragmentState(
            module=fs_module,
            entry_point="main",
            target_count=1,
            targets=color_targets,
        )

        vertex_state = wgpu.VertexState(
            module=vs_module,
            entry_point="main",
            buffer_count=1,
            buffers=vertBufferLayouts,
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
        ]

        bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(bgl_entries),
            entries=bgl_entries,
        )

        bgl = self.device.create_bind_group_layout(bgl_desc)

        bind_group_layouts = [bgl]

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=1,
            bind_group_layouts=bind_group_layouts,
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            fragment=fragmentState,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

        view: wgpu.TextureView = self.texture.create_view()

        bindgroup_entries = [
            wgpu.BindGroupEntry(binding=0, sampler=self.sampler),
            wgpu.BindGroupEntry(binding=1, texture_view=view),
        ]

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Texture bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entry_count=2,
            entries=bindgroup_entries,
        )

        self.bindGroup = self.device.create_bind_group(bindGroupDesc)
        logger.debug(self.bindGroup)

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, "VERTEX", vertex_data, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer_from_ndarray(
            self.device, "INDEX", index_data, wgpu.BufferUsage.INDEX
        )

    def create_textures(self):
        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(1024, 1024, 1),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )
        self.texture = self.device.create_texture(descriptor)

        self.sampler = self.device.create_sampler()

        data = np.zeros((4 * 1024 * 1024,), dtype=np.uint8)
        for i in range(0, data.size):
            data[i] = i % 253

        self.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.TexelCopyTextureInfo(
                texture=self.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            data,
            # The layout of the texture
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=4 * 1024,
                rows_per_image=1024,
            ),
            # The texture size
            wgpu.Extent3D(1024, 1024, 1),
        )

    def render(self, renderer: Renderer):
        color_attachments = [
            wgpu.RenderPassColorAttachment(
                view=renderer.view,
                load_op=wgpu.LoadOp.CLEAR,
                store_op=wgpu.StoreOp.STORE,
                clear_value=wgpu.Color(0, 0, 0, 1),
            )
        ]

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=color_attachments,
        )

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bindGroup)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32)
        pass_enc.draw_indexed(3)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)


def main():
    TriangleTextureDemo().run()


if __name__ == "__main__":
    main()
