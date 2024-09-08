import os
from pathlib import Path

from loguru import logger
import glm

from crunge import engine

from .page import Page

class App(engine.App):
    kWidth = 1280
    kHeight = 640
    def __init__(self):
        super().__init__(glm.ivec2(self.kWidth, self.kHeight), "ImGui Demo", resizable=True)
        self.pages: dict[str, Page] = {}
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
            self.page = page = entry['klass'].produce(self, name, entry['title'])
            self.show_view(page)
        self.schedule_once(callback, 0)
