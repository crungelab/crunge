import os, sys
import ctypes
from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p
from pathlib import Path

from loguru import logger
import glm

from crunge import sdl
from crunge import wgpu
from crunge.wgpu import utils

from crunge import imgui
from crunge import imnodes

from crunge import engine
from crunge.engine import Scheduler

from .page import Page

class App(engine.App):
    kWidth = 1280
    kHeight = 640
    def __init__(self):
        super().__init__(glm.ivec2(self.kWidth, self.kHeight), "ImFlo Demo", resizable=True)
        #self.pages = {}
        self.show_metrics = False
        self.show_style_editor = False
        self.resource_path = Path(__file__).parent.parent / 'resources'
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        imnodes.create_context()
        imnodes.push_attribute_flag(imnodes.AttributeFlags.ENABLE_LINK_DETACH_WITH_DRAG_CLICK)
        #TODO:Looks too scary to wrap.
        #io = imnodes.get_io()
        #io.link_detach_with_modifier_click.modifier = imgui.get_io().key_ctrl

    @property
    def page(self) -> Page:
        return self.view
    
    @page.setter
    def page(self, value: Page) -> None:
        self.view = value

    def use(self, name):
        logger.debug(f"use {name}")
        import importlib.util
        spec = importlib.util.find_spec(f"imflodemo.pages.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)

    '''
    def add_page(self, klass, name, title):
        self.pages[name] = { 'klass': klass, 'name': name, 'title': title }

    def show(self, name):
        logger.debug(f"show {name}")
        def callback(delta_time):
            entry = self.pages[name]
            self.page = page = entry['klass'].produce(self, name, entry['title'])
            #self.show_view(page)
        #self.schedule_once(callback, 0)
        Scheduler().schedule_once(callback, 0)
    '''