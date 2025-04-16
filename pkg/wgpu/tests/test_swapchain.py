import ctypes
import time
import sys

import glfw
from glfw import _glfw as glfw_native

from crunge import wgpu
from crunge.core import as_capsule

device: wgpu.Device = None
queue: wgpu.Queue = None
readbackBuffer: wgpu.Buffer = None
pipeline: wgpu.RenderPipeline = None

swapChain: wgpu.SwapChain = None
canvasDepthStencilView: wgpu.TextureView = None
kWidth: int = 800
kHeight: int = 600

def main():
    glfw.init()

    glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)

    window = glfw.create_window(kWidth, kHeight, "Test", None, None)

    #glfw.set_window_size_callback(self.window, self._handle_window_resize)

    wsd = None

    if sys.platform == "darwin":
        handle = glfw.get_cocoa_window(window)
    elif sys.platform == "win32":
        wsd = wgpu.SurfaceDescriptorFromWindowsHWND()
        handle = glfw.get_win32_window(window)
        wsd.hwnd = as_capsule(handle)
        wsd.hinstance = None
    elif sys.platform == "linux":
        #wsd = wgpu.SurfaceDescriptorFromXlibWindow()
        wsd = wgpu.SurfaceSourceXlibWindow()
        handle = glfw.get_x11_window(window)
        display = glfw.get_x11_display()
        wsd.window = handle
        wsd.display = as_capsule(display)

    instance = wgpu.create_instance()
    adapter = instance.request_adapter()
    props = adapter.get_properties()
    print(props.vendor_name)
    device = adapter.create_device()
    print(device)
    device.enable_logging()

    sd = wgpu.SurfaceDescriptor()
    sd.next_in_chain = wsd

    surface = instance.create_surface(sd)
    print(surface)

    scDesc = wgpu.SwapChainDescriptor()
    scDesc.usage = wgpu.TextureUsage.RENDER_ATTACHMENT
    scDesc.format = wgpu.TextureFormat.BGRA8_UNORM
    scDesc.width = kWidth
    scDesc.height = kHeight
    scDesc.present_mode = wgpu.PresentMode.FIFO
    swapChain = device.create_swap_chain(surface, scDesc)
    print(swapChain)

    last_time = time.perf_counter()
    target_frame_time = 1 / 60  # Target frame time for 60 FPS

    while not glfw.window_should_close(window):
        #instance.process_events()
        glfw.poll_events()

        now = time.perf_counter()
        frame_time = now - last_time

        # Calculate how much time is left to delay to maintain 60 FPS
        time_left = target_frame_time - frame_time

        # If there's time left in this frame, delay the next frame
        if time_left > 0:
            time.sleep(time_left)

        # Update last_time for the next frame, considering the sleep
        last_time = time.perf_counter()

        #self.update(frame_time)

    device.destroy()
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
