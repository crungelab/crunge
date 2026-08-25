from loguru import logger

from crunge.engine.imgui import ImGuiScreen
from ..view.view_2d import View2D

class Screen2D(ImGuiScreen):
    def __init__(self, name: str = "Screen2D", title: str = "Screen 2D") -> None:
        super().__init__(name=name, title=title)

    def create_children(self):
        logger.debug("Creating screen children")
        self.view = View2D()
        self.add_child(self.view)
