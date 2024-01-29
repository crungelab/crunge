from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .view import View

from loguru import logger

from .widget import Widget
from .renderer import Renderer
from .render_context import RenderContext

class Layer(Widget):
    def __init__(self, name: str, renderer: Renderer = None) -> None:
        super().__init__()
        self.name = name
        self.view: "View" = None
        self.renderer: Renderer = renderer

    def create(self, view: "View"):
        logger.debug("Layer.create")
        self.view = view
        self.width = view.width
        self.height = view.height

    def pre_draw(self):
        if self.renderer is not None:
            self.renderer.pre_draw()
        super().pre_draw()

    def draw(self):
        if self.renderer is not None:
            self.renderer.draw()
        super().draw()

    def post_draw(self):
        if self.renderer is not None:
            self.renderer.post_draw()
        super().post_draw()

    @property
    def window(self):
        return self.view.window
