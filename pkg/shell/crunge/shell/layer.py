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

    def render(self, context: RenderContext):
        if self.renderer is not None:
            self.renderer.render(context)
        super().render(context)

    @property
    def window(self):
        return self.view.window
