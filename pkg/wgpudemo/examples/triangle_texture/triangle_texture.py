import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys

from loguru import logger
import glfw
import numpy as np

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

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


class HelloWgpu:
    device: wgpu.Device = None
    queue: wgpu.Queue = None
    readback_buffer: wgpu.Buffer = None
    pipeline: wgpu.RenderPipeline = None

    surface: wgpu.Surface = None
    swap_chain: wgpu.SwapChain = None
    depth_stencil_view: wgpu.TextureView = None

    index_buffer: wgpu.Buffer = None
    vertex_buffer: wgpu.Buffer = None

    texture: wgpu.Texture = None
    sampler: wgpu.Sampler = None

    kWidth = 800
    kHeight = 600

    def __init__(self):
        self.instance = wgpu.create_instance()
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        self.device.enable_logging()
        self.queue = self.device.queue

        self.create_buffers()
        self.create_textures()

        vs_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, vs_shader_code
        )
        fs_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, fs_shader_code
        )

        vertAttributes = wgpu.VertexAttributes(
            [
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X4, offset=0, shader_location=0
                ),
                wgpu.VertexAttribute(
                    format=wgpu.VertexFormat.FLOAT32X4,
                    offset=4 * sizeof(c_float),
                    shader_location=1,
                ),
            ]
        )

        vertBufferLayout = wgpu.VertexBufferLayout(
            array_stride=8 * sizeof(c_float),
            attribute_count=2,
            attributes=vertAttributes[0],
        )

        colorTargetState = wgpu.ColorTargetState(
            format=wgpu.TextureFormat.BGRA8_UNORM,
        )

        fragmentState = wgpu.FragmentState(
            module=fs_module,
            entry_point="main",
            target_count=1,
            targets=colorTargetState,
        )

        vertex_state = wgpu.VertexState(
            module=vs_module,
            entry_point="main",
            buffer_count=1,
            buffers=vertBufferLayout,
        )

        bgl_entries = wgpu.BindGroupLayoutEntries(
            [
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
        )

        bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(bgl_entries), entries=bgl_entries[0]
        )
        bgl = self.device.create_bind_group_layout(bgl_desc)

        pl_desc = wgpu.PipelineLayoutDescriptor(
            bind_group_layout_count=1, bind_group_layouts=bgl
        )

        descriptor = wgpu.RenderPipelineDescriptor(
            label="Main Render Pipeline",
            layout=self.device.create_pipeline_layout(pl_desc),
            vertex=vertex_state,
            fragment=fragmentState,
        )

        self.pipeline = self.device.create_render_pipeline(descriptor)

        view: wgpu.TextureView = self.texture.create_view()

        bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=0, sampler=self.sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=view),
            ]
        )

        bindGroupDesc = wgpu.BindGroupDescriptor(
            label="Texture bind group",
            layout=self.pipeline.get_bind_group_layout(0),
            entry_count=2,
            entries=bindgroup_entries[0],
        )

        self.bindGroup = self.device.create_bind_group(bindGroupDesc)
        logger.debug(self.bindGroup)

        # exit()

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.kWidth, self.kHeight, "Hello", None, None)

    def create_buffers(self):
        self.index_buffer = utils.create_buffer_from_ndarray(
            self.device, index_data, wgpu.BufferUsage.INDEX
        )
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.device, vertex_data, wgpu.BufferUsage.VERTEX
        )
    """
    def create_textures(self):
        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(1024, 1024, 1),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count = 1,
            usage = wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING
        )
        self.texture = self.device.create_texture(descriptor)

        self.sampler = self.device.create_sampler()

        data = np.zeros((4 * 1024 * 1024,), dtype=np.uint8)
        for i in range(0, data.size):
            data[i] = i % 253

        staging_buffer = utils.create_buffer_from_ndarray(
            self.device, data, wgpu.BufferUsage.COPY_SRC
        )
        image_copy_buffer = utils.create_image_copy_buffer(staging_buffer, 0, 4 * 1024)
        image_copy_texture = utils.create_image_copy_texture(self.texture)
        copy_size = wgpu.Extent3D(1024, 1024, 1)

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        encoder.copy_buffer_to_texture(image_copy_buffer, image_copy_texture, copy_size)

        copy: wgpu.CommandBuffer = encoder.finish()
        self.queue.submit(1, copy)
    """
    def create_textures(self):
        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(1024, 1024, 1),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count = 1,
            usage = wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING
        )
        self.texture = self.device.create_texture(descriptor)

        self.sampler = self.device.create_sampler()

        data = np.zeros((4 * 1024 * 1024,), dtype=np.uint8)
        for i in range(0, data.size):
            data[i] = i % 253

        # The OLD way:
        """
        staging_buffer = utils.create_buffer_from_ndarray(
            self.device, data, wgpu.BufferUsage.COPY_SRC
        )
        image_copy_buffer = utils.create_image_copy_buffer(staging_buffer, 0, 4 * 1024)
        image_copy_texture = utils.create_image_copy_texture(self.texture)
        copy_size = wgpu.Extent3D(1024, 1024, 1)

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        encoder.copy_buffer_to_texture(image_copy_buffer, image_copy_texture, copy_size)

        copy: wgpu.CommandBuffer = encoder.finish()
        self.queue.submit(1, copy)
        """
        # The NEW way:
        self.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.ImageCopyTexture(
                texture=self.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            utils.as_capsule(data),
            # Data size
            data.size,
            # The layout of the texture
            wgpu.TextureDataLayout(
                offset=0,
                bytes_per_row=4 * 1024,
                rows_per_image=1024,
            ),
            #The texture size
            wgpu.Extent3D(1024, 1024, 1),
        )
        
    def create_swapchain(self):
        handle, display = None, None

        if sys.platform == "darwin":
            handle = glfw.get_cocoa_window(self.window)
        elif sys.platform == "win32":
            handle = glfw.get_win32_window(self.window)
        elif sys.platform == "linux":
            handle = glfw.get_x11_window(self.window)
            display = glfw.get_x11_display()

        logger.debug(handle)

        nwh = as_capsule(handle)
        logger.debug(nwh)

        wsd = wgpu.SurfaceDescriptorFromWindowsHWND()
        wsd.hwnd = nwh
        wsd.hinstance = None

        sd = wgpu.SurfaceDescriptor(next_in_chain=wsd)
        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)

        scDesc = wgpu.SwapChainDescriptor(
            usage=wgpu.TextureUsage.RENDER_ATTACHMENT,
            format=wgpu.TextureFormat.BGRA8_UNORM,
            width=self.kWidth,
            height=self.kHeight,
            present_mode=wgpu.PresentMode.MAILBOX,
        )

        self.swap_chain = self.device.create_swap_chain(self.surface, scDesc)
        logger.debug(self.swap_chain)

    def render(self, view: wgpu.TextureView):
        attachment = wgpu.RenderPassColorAttachment(
            view=view,
            load_op=wgpu.LoadOp.CLEAR,
            store_op=wgpu.StoreOp.STORE,
            clear_value=wgpu.Color(0, 0, 0, 1),
        )

        renderpass = wgpu.RenderPassDescriptor(
            label="Main Render Pass",
            color_attachment_count=1,
            color_attachments=attachment,
        )

        commands = wgpu.CommandBuffer()
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

    def frame(self):
        backbuffer: wgpu.TextureView = self.swap_chain.get_current_texture_view()
        backbuffer.set_label("Back Buffer Texture View")
        self.render(backbuffer)
        self.swap_chain.present()

    def run(self):
        self.create_window()
        self.create_swapchain()

        last_time = None
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            now = time.perf_counter()
            if not last_time:
                last_time = now

            frame_time = now - last_time
            last_time = now

            self.frame()

        glfw.destroy_window(self.window)
        glfw.terminate()


def main():
    HelloWgpu().run()


if __name__ == "__main__":
    main()
