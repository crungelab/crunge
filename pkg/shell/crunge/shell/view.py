from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .window import Window

from .widget import Widget
from .layer import Layer

class View(Widget):
    def __init__(self, window: "Window") -> None:
        super().__init__(window.width, window.height)
        self.window = window
        self.layers: Dict[str, Layer] = {}

    def add_layer(self, layer: Layer):
        self.layers[layer.name] = layer
        self.add_child(layer)

    def remove_layer(self, layer: Layer):
        self.layers.pop(layer.name)
        self.remove_child(layer)

    def get_layer(self, name: str) -> Layer:
        return self.layers[name]