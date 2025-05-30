import os
from pathlib import Path

from loguru import logger
import glm

from crunge import engine
from crunge.engine.resource.resource_manager import ResourceManager
from .page import Page

class Demo(engine.App):
    kWidth = 1280
    kHeight = 800
    def __init__(self, name: str, resource_root: Path):
        super().__init__(glm.ivec2(self.kWidth, self.kHeight), name, resizable=True)
        self.show_metrics = False
        self.show_style_editor = False
        self.resource_root = resource_root
        ResourceManager().add_path_variables(
            resources=self.resource_root,
        )

        #file_path = os.path.dirname(os.path.abspath(__file__))
        #os.chdir(file_path)

    @property
    def page(self) -> Page:
        return self.view
    
    @page.setter
    def page(self, value: Page) -> None:
        self.view = value

    def use(self, name):
        logger.debug(f"use {name}")
        import importlib.util
        spec = importlib.util.find_spec(f"imdemo.pages.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)
