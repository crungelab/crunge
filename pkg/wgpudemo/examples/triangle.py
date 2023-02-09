import ctypes
import time
import sys

from loguru import logger
import glfw
import numpy as np


from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge.core import as_capsule

shader_code = """
@vertex
fn main_v(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
    var pos = array<vec2<f32>, 3>(
        vec2<f32>(0.0, 0.5), vec2<f32>(-0.5, -0.5), vec2<f32>(0.5, -0.5));
    return vec4<f32>(pos[idx], 0.0, 1.0);
}
@fragment
fn main_f() -> @location(0) vec4<f32> {
    return vec4<f32>(0.0, 0.502, 1.0, 1.0); // 0x80/0xff ~= 0.502
}

"""
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
    return textureSample(myTexture, mySampler, FragCoord.xy / vec2<f32>(640.0, 480.0));
}
"""

index_data = np.array([0, 1, 2], dtype=np.uint32)

vertex_data = np.array([
    0.0, 0.5, 0.0, 1.0, -0.5, -0.5, 0.0, 1.0, 0.5, -0.5, 0.0, 1.0,
], dtype=np.float32)


class HelloTriangle:
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

        vs_module: wgpu.ShaderModule = utils.create_shader_module(self.device, vs_shader_code)
        fs_module: wgpu.ShaderModule = utils.create_shader_module(self.device, fs_shader_code)

        """
            auto bgl = utils::MakeBindGroupLayout(
                device, {
                            {0, wgpu::ShaderStage::Fragment, wgpu::SamplerBindingType::Filtering},
                            {1, wgpu::ShaderStage::Fragment, wgpu::TextureSampleType::Float},
                        });

        """
        """
        wgsl_desc = wgpu.ShaderModuleWGSLDescriptor()
        wgsl_desc.source = shader_code
        descriptor = wgpu.ShaderModuleDescriptor()
        descriptor.next_in_chain = wgsl_desc
        shader_module = self.device.create_shader_module(descriptor)

        bgl_desc = wgpu.BindGroupLayoutDescriptor()
        bgl = self.device.create_bind_group_layout(bgl_desc)
        desc = wgpu.BindGroupDescriptor()
        desc.layout = bgl
        desc.entry_count = 0
        desc.entries = None
        bg = self.device.create_bind_group(desc)

        pl = wgpu.PipelineLayoutDescriptor()
        pl.bind_group_layout_count = 0
        pl.bind_group_layouts = None

        colorTargetState = wgpu.ColorTargetState()
        colorTargetState.format = wgpu.TextureFormat.BGRA8_UNORM

        fragmentState = wgpu.FragmentState()
        fragmentState.module = shader_module
        fragmentState.entry_point = "main_f"
        fragmentState.target_count = 1
        fragmentState.targets = colorTargetState

        depthStencilState = wgpu.DepthStencilState()
        depthStencilState.format = wgpu.TextureFormat.DEPTH32_FLOAT

        descriptor = wgpu.RenderPipelineDescriptor()
        descriptor.layout = self.device.create_pipeline_layout(pl)
        descriptor.vertex.module = shader_module
        descriptor.vertex.entry_point = "main_v"
        descriptor.fragment = fragmentState
        descriptor.primitive.topology = wgpu.PrimitiveTopology.TRIANGLE_LIST
        descriptor.depth_stencil = depthStencilState
        self.pipeline = self.device.create_render_pipeline(descriptor)
        logger.debug(self.pipeline)
        """

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.kWidth, self.kHeight, "Hello", None, None)

    def create_buffers(self):
        self.index_buffer = utils.create_buffer_from_ndarray(self.device, index_data, wgpu.BufferUsage.INDEX)
        self.vertex_buffer = utils.create_buffer_from_ndarray(self.device, vertex_data, wgpu.BufferUsage.VERTEX)

    def create_textures(self):
        descriptor = wgpu.TextureDescriptor()
        descriptor.dimension = wgpu.TextureDimension.E2_D
        descriptor.size.width = 1024
        descriptor.size.height = 1024
        descriptor.size.depth_or_array_layers = 1
        descriptor.sample_count = 1
        descriptor.format = wgpu.TextureFormat.RGBA8_UNORM
        descriptor.mip_level_count = 1
        descriptor.usage = wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING
        texture = self.device.create_texture(descriptor)

        sampler = self.device.create_sampler()

        data = np.zeros((4 * 1024 * 1024,), dtype=np.uint32)
        for i in range(0, data.size):
            data[i] = (i % 253)

        staging_buffer = utils.create_buffer_from_ndarray(self.device, data, wgpu.BufferUsage.COPY_SRC)
        image_copy_buffer = utils.create_image_copy_buffer(staging_buffer, 0, 4 * 1024)
        image_copy_texture = utils.create_image_copy_texture(texture)
        copy_size = wgpu.Extent3D(1024, 1024, 1)

        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        encoder.copy_buffer_to_texture(image_copy_buffer, image_copy_texture, copy_size)

        copy: wgpu.CommandBuffer = encoder.finish()
        self.queue.submit(1, copy)
        
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

        sd = wgpu.SurfaceDescriptor()
        sd.next_in_chain = wsd

        self.surface = self.instance.create_surface(sd)
        logger.debug(self.surface)

        scDesc = wgpu.SwapChainDescriptor()
        scDesc.usage = wgpu.TextureUsage.RENDER_ATTACHMENT
        scDesc.format = wgpu.TextureFormat.BGRA8_UNORM
        scDesc.width = 800
        scDesc.height = 600
        scDesc.present_mode = wgpu.PresentMode.FIFO
        self.swap_chain = self.device.create_swap_chain(self.surface, scDesc)
        logger.debug(self.swap_chain)

    def create_depth_stencil_view(self):
        descriptor = wgpu.TextureDescriptor()
        descriptor.usage = wgpu.TextureUsage.RENDER_ATTACHMENT
        descriptor.size = wgpu.Extent3D(self.kWidth, self.kHeight, 1)
        descriptor.format = wgpu.TextureFormat.DEPTH32_FLOAT
        self.depth_stencil_view = self.device.create_texture(descriptor).create_view()

    def render(self, view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
        attachment = wgpu.RenderPassColorAttachment()
        attachment.view = view
        attachment.load_op = wgpu.LoadOp.CLEAR
        attachment.store_op = wgpu.StoreOp.STORE
        attachment.clear_value = wgpu.Color(0, 0, 0, 1)

        renderpass = wgpu.RenderPassDescriptor()
        renderpass.color_attachment_count = 1
        renderpass.color_attachments = attachment
        # renderpass.color_attachments = [attachment] #TODO:  Pointer to array

        depth_stencil_attachment = wgpu.RenderPassDepthStencilAttachment()
        depth_stencil_attachment.view = depthStencilView
        depth_stencil_attachment.depth_clear_value = 0
        depth_stencil_attachment.depth_load_op = wgpu.LoadOp.CLEAR
        depth_stencil_attachment.depth_store_op = wgpu.StoreOp.STORE

        renderpass.depth_stencil_attachment = depth_stencil_attachment

        commands = wgpu.CommandBuffer()
        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.draw(3)
        pass_enc.end()
        commands = encoder.finish()

        self.queue.submit(1, commands)

    def frame(self):
        backbuffer: wgpu.TextureView = self.swap_chain.get_current_texture_view()
        self.render(backbuffer, self.depth_stencil_view)
        self.swap_chain.present()

    def run(self):
        self.create_window()
        self.create_swapchain()
        self.create_depth_stencil_view()

        last_time = None
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            now = time.perf_counter()
            if not last_time:
                last_time = now

            frame_time = now - last_time
            last_time = now

            self.frame()
            # exit()

        glfw.destroy_window(self.window)
        glfw.terminate()


if __name__ == "__main__":
    HelloTriangle().run()
