from loguru import logger
import glm

from .widget import Widget
from .view import View


class Frame(Widget):
    def __init__(self, size=glm.ivec2(), view: View = None) -> None:
        super().__init__(size)
        self.view = view

    def resize(self, size: glm.ivec2):
        super().resize(size)
        if self.view is not None:
            self.view.resize(size)

    def create(self):
        logger.debug("Frame.create")
        if self.view is not None:
            self.view.create(self)
            self.show_view(self.view)
        return self

    def show_view(self, view: View):
        self.view = view
        self.children.clear()
        self.add_child(view)
