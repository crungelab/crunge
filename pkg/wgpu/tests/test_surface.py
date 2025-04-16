import ctypes
import time
import sys

import glfw

from crunge import wgpu
from crunge.core import as_capsule

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
    glfw.window_hint(glfw.RESIZABLE, True)

    window = glfw.create_window(800, 600, "Test", None, None)

    # glfw.set_window_size_callback(self.window, self._handle_window_resize)

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
    sd.label = "Test Surface"
    print(sd.label)
    sd.next_in_chain = wsd

    surface = instance.create_surface(sd)
    print(surface)

    last_time = time.perf_counter()
    target_frame_time = 1 / 60  # Target frame time for 60 FPS

    while not glfw.window_should_close(window):
        # instance.process_events()
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

    device.destroy()
    glfw.destroy_window(window)
    glfw.terminate()


if __name__ == "__main__":
    main()
