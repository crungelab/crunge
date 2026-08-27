from loguru import logger

from ...screen import Screen

from ..view.view_2d import View2D


class Screen2D(Screen):
    def __init__(self, name: str = "Screen2D", title: str = "Screen 2D") -> None:
        super().__init__(name=name, title=title)

    def create_views(self):
        self.view = View2D()
        self.add_child(self.view)
