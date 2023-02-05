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

    wsd = wgpu.SurfaceDescriptorFromWindowsHWND()
    wsd.hwnd = nwh
    wsd.hinstance = None

    sd = wgpu.SurfaceDescriptor()
    sd.next_in_chain = wsd

    surface = instance.create_surface(sd)
    print(surface)

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


if __name__ == "__main__":
    main()