import ctypes
import time
import sys
from loguru import logger
import glfw

from crunge import bgfx
from crunge.core import as_capsule

class Window:
    def __init__(self, width, height, title):
        self.title = title
        self.height = height
        self.width = width
        self.window = None

    def init(self, platform_data):
        pass

    def shutdown(self):
        pass

    def update(self, dt):
        pass

    def resize(self, width, height):
        pass

    def get_mouse_state(self):
        mouse_x, mouse_y = glfw.get_cursor_pos(self.window)
        state_mbl = glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_LEFT)
        state_mbm = glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_MIDDLE)
        state_mbr = glfw.get_mouse_button(self.window, glfw.MOUSE_BUTTON_RIGHT)

        return (
            mouse_x,
            mouse_y,
            1
            if state_mbl == glfw.PRESS
            else 0 | 1
            if state_mbm == glfw.PRESS
            else 0 | 1
            if state_mbr == glfw.PRESS
            else 0,
        )

    def run(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)

        self.window = glfw.create_window(
            self.width, self.height, self.title, None, None
        )

        glfw.set_window_size_callback(self.window, self._handle_window_resize)

        handle, display = None, None

        if sys.platform == "darwin":
            handle = glfw.get_cocoa_window(self.window)
        elif sys.platform == "win32":
            handle = glfw.get_win32_window(self.window)
        elif sys.platform == "linux":
            handle = glfw.get_x11_window(self.window)
            display = glfw.get_x11_display()

        logger.debug(handle)
        
        data = bgfx.PlatformData()
        data.ndt = as_capsule(display) if display else None
        data.nwh = as_capsule(handle)
        logger.debug(data.nwh)
        data.context = None
        data.back_buffer = None
        data.back_buffer_ds = None

        print(data.nwh)
        self.init(data)

        last_time = None

        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            now = time.perf_counter()
            if not last_time:
                last_time = now

            frame_time = now - last_time
            last_time = now

            self.update(frame_time)

        self.shutdown()
        glfw.destroy_window(self.window)
        glfw.terminate()

    def _handle_window_resize(self, window, width, height):
        self.width = width
        self.height = height

        self.resize(width, height)
