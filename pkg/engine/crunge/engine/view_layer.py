from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .view import View

from loguru import logger

from .widget import Widget
from .renderer import Renderer
from .vu import Vu


class ViewLayer(Widget):
    def __init__(self, name: str, priority: int = 0, vu: Vu = None) -> None:
        super().__init__()
        self.name = name
        self.priority = priority
        self.view: "View" = None
        self.vu = vu

    def set_view(self, view):
        self.view = view
        return self

    def _create(self):
        logger.debug("Layer.create")
        self.size = self.view.size

    @property
    def window(self):
        return self.view.window
