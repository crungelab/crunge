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
        pass

    def create_window(self):
        glfw.init()

        glfw.window_hint(glfw.CLIENT_API, glfw.NO_API)
        glfw.window_hint(glfw.RESIZABLE, True)

        self.window = glfw.create_window(self.kWidth, self.kHeight, "GlTF Viewer", None, None)

    def create_view(self, scene: Scene):
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

        view = View(scene, self.kWidth, self.kHeight)
        view.create_from_windows_hwnd(nwh)
        self.view = view

    def show(self, scene: Scene):
        self.scene = scene
        self.create_window()
        self.create_view(scene)

        last_time = None
        while not glfw.window_should_close(self.window):
            glfw.poll_events()

            now = time.perf_counter()
            if not last_time:
                last_time = now

            frame_time = now - last_time
            last_time = now

            self.view.frame()

        glfw.destroy_window(self.window)
        glfw.terminate()
