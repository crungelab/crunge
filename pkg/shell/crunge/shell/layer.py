from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .view import View

from .widget import Widget

class Layer(Widget):
    def __init__(self, view: "View", name: str) -> None:
        super().__init__(view.width, view.height)
        self.view = view
        self.window = view.window
        self.name = name

    def create(self):
        pass