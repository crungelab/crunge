import os, sys
import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
from pathlib import Path

from loguru import logger
import glm

from crunge import shell

from crunge import as_capsule
from crunge import sdl, wgpu
import crunge.wgpu.utils as utils

from crunge import imgui

class App(shell.App):
    def __init__(self):
        super().__init__(1280, 640, "ImGui Demo", resizable=True)
        self.pages = {}
        self.show_metrics = False
        self.show_style_editor = False
        self.resource_path = Path(__file__).parent.parent / 'resources'
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def use(self, name):
        logger.debug(f"use {name}")
        import importlib.util
        spec = importlib.util.find_spec(f"imdemo.pages.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)

    def add_page(self, klass, name, title):
        self.pages[name] = { 'klass': klass, 'name': name, 'title': title }

    def show(self, name):
        logger.debug(f"show {name}")
        def callback(delta_time):
            entry = self.pages[name]
            self.page = page = entry['klass'].create(self, name, entry['title'])
            self.show_view(page)
        self.schedule_once(callback, 0)
            

    def frame(self):
        #logger.debug("frame")
        self.pre_draw()
        self.draw()
        self.post_draw()

        backbuffer: wgpu.TextureView = self.swap_chain.get_current_texture_view()
        backbuffer.set_label("Back Buffer Texture View")
        context = shell.RenderContext(self.device, backbuffer, self.depth_stencil_view)
        self.render(context)
        self.swap_chain.present()
