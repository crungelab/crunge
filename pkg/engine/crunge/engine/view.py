from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .window import Window

from loguru import logger
import glm

from .widget import Widget
from .layer import Layer

class View(Widget):
    def __init__(self, layers=[]) -> None:
        super().__init__()
        self.window = None
        self.layers: Dict[str, Layer] = {}
        for layer in layers:
            self.add_layer(layer)

    def resize(self, size: glm.ivec2):
        super().resize(size)
        for layer in self.layers.values():
            layer.resize(size)

    def create(self, window: "Window"):
        logger.debug("View.create")
        super().create()
        self.window = window
        self.width = window.width
        self.height = window.height
        for layer in self.layers.values():
            layer.create(self)
        return self

    def add_layer(self, layer: Layer):
        self.layers[layer.name] = layer
        self.add_child(layer)

    def remove_layer(self, layer: Layer):
        self.layers.pop(layer.name)
        self.remove_child(layer)

    def get_layer(self, name: str) -> Layer:
        return self.layers[name]