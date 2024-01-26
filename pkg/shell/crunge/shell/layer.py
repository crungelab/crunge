from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .view import View

from loguru import logger

from .widget import Widget

class Layer(Widget):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.view: "View" = None

    def create(self, view: "View"):
        logger.debug("Layer.create")
        self.view = view
        self.width = view.width
        self.height = view.height

    @property
    def window(self):
        return self.view.window