import ctypes
import time
import sys

from crunge import wgpu

import glfw
from glfw import _glfw as glfw_native

from utils import as_void_ptr

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

    #adapter = wgpu.Adapter()
    #device = wgpu.Adapter.create_device()
    #instance = wgpu.create_instance()
    #instance_descriptor = wgpu.InstanceDescriptor()
    #dawn_instance_descriptor = wgpu.DawnInstanceDescriptor()
    #instance_descriptor.next_in_chain = dawn_instance_descriptor
    #instance = wgpu.create_instance(instance_descriptor)
    instance = wgpu.create_instance(None)

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

if __name__ == "__main__":
    main()