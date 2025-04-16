import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
import time
import sys
import math
import glm
from pathlib import Path

from loguru import logger
import glfw
import numpy as np
import trimesh as tm
import networkx as nx

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from .base import Base
from .scene import Scene
from .view import View


class Viewer(Base):
    kWidth = 1024
    kHeight = 768
    
    def __init__(self):
        self.size = glm.ivec2(self.kWidth, self.kHeight)

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.kWidth, self.kHeight, "GlTF Viewer", None, None)

        def resize_cb(window, w, h):
            self.view.resize(glm.ivec2(w, h))
        glfw.set_window_size_callback(self.window, resize_cb)


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

        view = View(scene, self.size)
        view.create_from_wsd(wsd)
        self.view = view

    def show(self, scene: Scene):
        self.scene = scene
        self.create_window()
        self.create_view(scene)

        last_time = time.perf_counter()
        target_frame_time = 1 / 60  # Target frame time for 60 FPS

        while not glfw.window_should_close(self.window):
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

            self.view.frame()

        glfw.destroy_window(self.window)
        glfw.terminate()
