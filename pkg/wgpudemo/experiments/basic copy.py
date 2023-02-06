import ctypes
import time
import sys

from crunge import wgpu

import glfw
from glfw import _glfw as glfw_native

from utils import as_void_ptr

device: wgpu.Device = None
queue: wgpu.Queue = None
readbackBuffer: wgpu.Buffer = None
pipeline: wgpu.RenderPipeline = None

swapChain: wgpu.SwapChain = None
canvasDepthStencilView: wgpu.TextureView = None
kWidth: int = 300
kHeight: int = 150

shader_code = """
    @stage(vertex)
    fn main_v(@builtin(vertex_index) idx: u32) -> @builtin(position) vec4<f32> {
        var pos = array<vec2<f32>, 3>(
            vec2<f32>(0.0, 0.5), vec2<f32>(-0.5, -0.5), vec2<f32>(0.5, -0.5));
        return vec4<f32>(pos[idx], 0.0, 1.0);
    }
    @stage(fragment)
    fn main_f() -> @location(0) vec4<f32> {
        return vec4<f32>(0.0, 0.502, 1.0, 1.0); // 0x80/0xff ~= 0.502
    }
"""

def main():
    glfw.init()

    glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)

    window = glfw.create_window(800, 600, "Test", None, None)

    #glfw.set_window_size_callback(self.window, self._handle_window_resize)

    handle, display = None, None

    if sys.platform == "darwin":
        handle = glfw.get_cocoa_window(self.window)
    elif sys.platform == "win32":
        handle = glfw.get_win32_window(window)
    elif sys.platform == "linux":
        handle = glfw.get_x11_window(self.window)
        display = glfw.get_x11_display()

    nwh = as_void_ptr(handle)
    print(nwh)

    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    props = wgpu.AdapterProperties()
    adapter.get_properties(props)
    print(props.vendor_name)
    device = adapter.create_device()
    print(device)
    #feature_name = FeatureName()
    queue = device.get_queue()

    wgsl_desc = wgpu.ShaderModuleWGSLDescriptor()
    wgsl_desc.source = shader_code
    descriptor = wgpu.ShaderModuleDescriptor()
    descriptor.next_in_chain = wgsl_desc
    shader_module = device.create_shader_module(descriptor)

    bgl_desc = wgpu.BindGroupLayoutDescriptor()
    bgl = device.create_bind_group_layout(bgl_desc)
    desc = wgpu.BindGroupDescriptor()
    desc.layout = bgl
    desc.entry_count = 0
    desc.entries = None
    bg = device.create_bind_group(desc)

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
    descriptor.layout = device.create_pipeline_layout(pl)
    descriptor.vertex.module = shader_module
    descriptor.vertex.entry_point = "main_v"
    descriptor.fragment = fragmentState
    descriptor.primitive.topology = wgpu.PrimitiveTopology.TRIANGLE_LIST
    descriptor.depth_stencil = depthStencilState
    pipeline = device.create_render_pipeline(descriptor)
    print(pipeline)

    last_time = None
    while not glfw.window_should_close(window):
        glfw.poll_events()

        now = time.perf_counter()
        if not last_time:
            last_time = now

        frame_time = now - last_time
        last_time = now

        #self.update(frame_time)

    #self.shutdown()
    glfw.destroy_window(window)
    glfw.terminate()

def render(view: wgpu.TextureView, depthStencilView: wgpu.TextureView):
    attachment = wgpu.RenderPassColorAttachment()
    attachment.view = view
    attachment.load_op = wgpu.LoadOp.CLEAR
    attachment.store_op = wgpu.StoreOp.STORE
    attachment.clear_value = wgpu.Color(0, 0, 0, 1)

    renderpass = wgpu.RenderPassDescriptor()
    renderpass.color_attachment_count = 1
    renderpass.color_attachments = [attachment] #TODO:  Pointer to array

    depthStencilAttachment = wgpu.RenderPassDepthStencilAttachment()
    depthStencilAttachment.view = depthStencilView
    depthStencilAttachment.depth_clear_value = 0
    depthStencilAttachment.depth_load_op = wgpu.LoadOp.CLEAR
    depthStencilAttachment.depth_store_op = wgpu.StoreOp.STORE

    renderpass.depthStencilAttachment = depthStencilAttachment

    commands = wgpu.CommandBuffer()
    encoder: wgpu.CommandEncoder = device.create_command_encoder()
    pass_enc: wgpu.RenderPassEncoder = encoder.begin_render_pass(renderpass)
    pass_enc.set_pipeline(pipeline)
    pass_enc.draw(3)
    pass_enc.end()
    commands = encoder.finish()
    
    queue.submit(1, commands)

    def frame():
        backbuffer: wgpu.TextureView  = swapChain.get_current_texture_view()
        render(backbuffer, canvasDepthStencilView)
        swapChain.present()


"""
void render(wgpu::TextureView view, wgpu::TextureView depthStencilView) {
    wgpu::RenderPassColorAttachment attachment{};
    attachment.view = view;
    attachment.loadOp = wgpu::LoadOp::Clear;
    attachment.storeOp = wgpu::StoreOp::Store;
    attachment.clearValue = {0, 0, 0, 1};

    wgpu::RenderPassDescriptor renderpass{};
    renderpass.colorAttachmentCount = 1;
    renderpass.colorAttachments = &attachment;

    wgpu::RenderPassDepthStencilAttachment depthStencilAttachment = {};
    depthStencilAttachment.view = depthStencilView;
    depthStencilAttachment.depthClearValue = 0;
    depthStencilAttachment.depthLoadOp = wgpu::LoadOp::Clear;
    depthStencilAttachment.depthStoreOp = wgpu::StoreOp::Store;

    renderpass.depthStencilAttachment = &depthStencilAttachment;

    wgpu::CommandBuffer commands;
    {
        wgpu::CommandEncoder encoder = device.CreateCommandEncoder();
        {
            wgpu::RenderPassEncoder pass = encoder.BeginRenderPass(&renderpass);
            pass.SetPipeline(pipeline);
            pass.Draw(3);
            pass.End();
        }
        commands = encoder.Finish();
    }

    queue.Submit(1, &commands);
}

"""
if __name__ == "__main__":
    main()