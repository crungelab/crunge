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

index_data = np.array([0, 1, 2], dtype=np.uint32)

vertex_data = np.array([
    0.0, .5, 0.0, 1.0, 1.0, 0.0,  0.0, 1.0, -.5, -.5, 0., 1.0,
    0.0, 1.0, 0.0, 1.0, .5, -.5, 0.0, 1.0, 0.0,  0.0,  1.0, 1.0,
], dtype=np.float32)


shader_code = """
struct VertexInput {
  @location(0) pos: vec4<f32>,
  @location(1) color: vec4<f32>,
}

struct VertexOutput {
  @builtin(position) pos: vec4<f32>,
  @location(0) color: vec4<f32>,
}

@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
  return VertexOutput(in.pos, in.color);
}

@fragment
fn fs_main(in : VertexOutput) -> @location(0) vec4<f32> {
  return in.color;
}
"""


class HelloWgpu:
    device: wgpu.Device = None
    queue: wgpu.Queue = None
    readbackBuffer: wgpu.Buffer = None
    pipeline: wgpu.RenderPipeline = None

    surface: wgpu.Surface = None
    swap_chain: wgpu.SwapChain = None
    depth_stencil_view: wgpu.TextureView = None

    vertex_buffer: wgpu.Buffer = None

    kWidth = 1024
    kHeight = 768

    def __init__(self):
        self.instance = wgpu.create_instance()
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        self.device.enable_logging()
        self.queue = self.device.get_queue()

        self.create_buffers()

        shader_module: wgpu.ShaderModule = utils.create_shader_module(self.device, shader_code)

        # Pipeline creation

        # TODO: Need to implement kwargs initializers
        va0 = wgpu.VertexAttribute()
        va0.format = wgpu.VertexFormat.FLOAT32X4
        va0.offset = 0
        va0.shader_location = 0
        
        va1 = wgpu.VertexAttribute()
        va1.format = wgpu.VertexFormat.FLOAT32X4
        va1.offset = 4 * sizeof(c_float)
        va1.shader_location = 1

        vertAttributes = wgpu.VertexAttributes([va0, va1])
        
        vertBufferLayout = wgpu.VertexBufferLayout()
        vertBufferLayout.array_stride = 8 * sizeof(c_float)
        vertBufferLayout.attribute_count = 2
        vertBufferLayout.attributes = vertAttributes[0]

        colorTargetState = wgpu.ColorTargetState()
        colorTargetState.format = wgpu.TextureFormat.BGRA8_UNORM

        fragmentState = wgpu.FragmentState()
        fragmentState.module = shader_module
        fragmentState.entry_point = "fs_main"
        fragmentState.target_count = 1
        fragmentState.targets = colorTargetState

        pl = wgpu.PipelineLayoutDescriptor()
        pl.bind_group_layout_count = 0
        pl.bind_group_layouts = None

        descriptor = wgpu.RenderPipelineDescriptor()
        descriptor.label = "Main Render Pipeline"
        #descriptor.layout = None # Automatic layout #TODO: ?
        descriptor.layout = self.device.create_pipeline_layout(pl)
        descriptor.vertex.module = shader_module
        descriptor.vertex.entry_point = "vs_main"
        descriptor.vertex.buffer_count = 1
        descriptor.vertex.buffers = vertBufferLayout
        descriptor.fragment = fragmentState
        self.pipeline = self.device.create_render_pipeline(descriptor)

    def create_buffers(self):
        self.index_buffer = utils.create_buffer_from_ndarray(self.device, index_data, wgpu.BufferUsage.INDEX)
        self.vertex_buffer = utils.create_buffer_from_ndarray(self.device, vertex_data, wgpu.BufferUsage.VERTEX)

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.kWidth, self.kHeight, "Hello", None, None)

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
        scDesc.width = self.kWidth
        scDesc.height = self.kHeight
        #scDesc.present_mode = wgpu.PresentMode.FIFO
        scDesc.present_mode = wgpu.PresentMode.MAILBOX
        self.swap_chain = self.device.create_swap_chain(self.surface, scDesc)
        logger.debug(self.swap_chain)

    def create_depth_stencil_view(self):
        descriptor = wgpu.TextureDescriptor()
        descriptor.usage = wgpu.TextureUsage.RENDER_ATTACHMENT
        descriptor.size = wgpu.Extent3D(self.kWidth, self.kHeight, 1)
        descriptor.format = wgpu.TextureFormat.DEPTH32_FLOAT
        self.depth_stencil_view = self.device.create_texture(descriptor).create_view()

    def render(self, view: wgpu.TextureView):
        attachment = wgpu.RenderPassColorAttachment()
        attachment.view = view
        attachment.load_op = wgpu.LoadOp.CLEAR
        attachment.store_op = wgpu.StoreOp.STORE
        attachment.clear_value = wgpu.Color(0, 0, 0, 1)

        renderpass = wgpu.RenderPassDescriptor()
        renderpass.label = "Main Render Pass"
        renderpass.color_attachment_count = 1
        renderpass.color_attachments = attachment

        commands = wgpu.CommandBuffer()
        encoder: wgpu.CommandEncoder = self.device.create_command_encoder()
        pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32);
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

        glfw.destroy_window(self.window)
        glfw.terminate()


if __name__ == "__main__":
    HelloWgpu().run()
