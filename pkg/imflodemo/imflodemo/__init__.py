import os

import pyglet
import arcade

from crunge import imgui
from crunge.imgui.impl.arcade import ArcadeGui

from crunge import imnodes

class App(arcade.Window):
    def __init__(self):
        super().__init__(1280, 640, "AimFlo Demo", resizable=True)
        self.gui = ArcadeGui(self)
        self.pages = {}
        self.show_metrics = False
        imnodes.create_context()
        imnodes.push_attribute_flag(imnodes.ATTRIBUTE_FLAGS_ENABLE_LINK_DETACH_WITH_DRAG_CLICK)
        io = imnodes.get_io()
        #TODO:Looks too scary to wrap.
        #io.link_detach_with_modifier_click.modifier = imgui.get_io().key_ctrl

    def on_draw(self):
        super().on_draw()
        self.gui.render()

    def run(self):
        arcade.run()

    def use(self, name):
        import importlib.util
        spec = importlib.util.find_spec(f"imflodemo.pages.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)

    def add_page(self, klass, name, title):
        self.pages[name] = { 'klass': klass, 'name': name, 'title': title }

    def show(self, name):
        def callback(delta_time):
            entry = self.pages[name]
            self.page = page = entry['klass'].create(self, name, entry['title'])
            self.show_view(page)
        pyglet.clock.schedule_once(callback, 0)