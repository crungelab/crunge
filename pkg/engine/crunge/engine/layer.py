from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .view import View

from loguru import logger

from .widget import Widget
from .renderer import Renderer
from .vu import Vu


class Layer(Widget):
    def __init__(self, name: str, vu: Vu = None) -> None:
        super().__init__()
        self.name = name
        self.view: "View" = None
        self.vu: Vu = vu

    def create(self, view: "View"):
        logger.debug("Layer.create")
        self.view = view
        self.size = view.size

    '''
    def pre_draw(self, renderer: Renderer):
        if self.vu is not None:
            self.vu.pre_draw(renderer)
        super().pre_draw(renderer)

    def draw(self, renderer: Renderer):
        if self.vu is not None:
            self.vu.draw(renderer)
        super().draw(renderer)

    def post_draw(self, renderer: Renderer):
        if self.vu is not None:
            self.vu.post_draw(renderer)
        super().post_draw(renderer)
    '''
    @property
    def window(self):
        return self.view.window
