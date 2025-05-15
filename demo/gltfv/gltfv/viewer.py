import time
import sys

from loguru import logger
import glfw
import glm

from crunge.core import as_capsule
from crunge import wgpu

import gltfv.globals as globals

from .base import Base
from .scene import Scene
from .view import View
from .camera import Camera
from .controller.camera import CameraController
from .controller.camera.arcball import ArcballCameraController


class Viewer(Base):
    kWidth = 1024
    kHeight = 768
    
    def __init__(self):
        self.camera: Camera = None
        self.camera_controller: CameraController = None
        self.delta_time = 0

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.kWidth, self.kHeight, "GlTF Viewer", None, None)

        glfw.set_cursor_pos_callback(self.window, self.on_cursor_pos)
        glfw.set_mouse_button_callback(self.window, self.on_mouse_button)
        glfw.set_scroll_callback(self.window, self.on_scroll)

        glfw.set_key_callback(self.window, self.on_key)

    def create_view(self, scene: Scene):
        wsd = None
        if sys.platform == "darwin":
            handle = glfw.get_cocoa_window(self.window)
        elif sys.platform == "win32":
            wsd = wgpu.SurfaceDescriptorFromWindowsHWND()
            handle = glfw.get_win32_window(self.window)
            wsd.hwnd = as_capsule(handle)
            wsd.hinstance = None

        elif sys.platform == "linux":
            #wsd = wgpu.SurfaceDescriptorFromXlibWindow()
            wsd = wgpu.SurfaceSourceXlibWindow()
            handle = glfw.get_x11_window(self.window)
            display = glfw.get_x11_display()
            wsd.window = handle
            wsd.display = as_capsule(display)

        view = View(scene, glm.ivec2(self.kWidth, self.kHeight))
        view.create_from_wsd(wsd)
        self.view = view

    def show(self, scene: Scene):
        self.scene = scene
        self.create_window()
        self.create_view(scene)

        self.camera = self.view.camera
        self.camera_controller = ArcballCameraController(self.window, self.camera)
        self.camera_controller.activate()

        last_time = time.perf_counter()
        target_frame_time = 1 / 60  # Target frame time for 60 FPS

        while not glfw.window_should_close(self.window):
            #Error: Assertion failure at /home/kurt/Dev/crunge/depot/dawn/src/dawn/native/EventManager.cpp:479 (WaitRef): !wasAlreadyWaited
            #globals.instance.process_events()

            glfw.poll_events()

            now = time.perf_counter()
            frame_time = now - last_time
            self.delta_time = frame_time
            self.camera_controller.update(frame_time)

            # Calculate how much time is left to delay to maintain 60 FPS
            time_left = target_frame_time - frame_time

            # If there's time left in this frame, delay the next frame
            if time_left > 0:
                time.sleep(time_left)

            # Update last_time for the next frame, considering the sleep
            last_time = time.perf_counter()

            self.view.frame()

        glfw.destroy_window(self.window)
        #glfw.terminate() # causes crash on exit

    def on_cursor_pos(self, window, xpos, ypos):
        self.camera_controller.on_cursor_pos(window, xpos, ypos)

    def on_mouse_button(self,window, button, action, mods):
        self.camera_controller.on_mouse_button(window, button, action, mods)

    def on_scroll(self, window, xoffset, yoffset):
        self.camera_controller.on_scroll(window, xoffset, yoffset)

    def on_key(self, window, key, scancode, action, mods):
        self.camera_controller.on_key(window, key, scancode, action, mods)
        if key == glfw.KEY_ESCAPE and action == glfw.PRESS:
            glfw.set_window_should_close(window, True)
