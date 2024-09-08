from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .window import Window

from loguru import logger
import glm

from .widget import Widget
from .layer import Layer

class View(Widget):
    def __init__(self, size=glm.ivec2(), layers=[]) -> None:
        super().__init__(size)
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
        self.size = window.size
        for layer in self.layers.values():
            layer.create(self)
        self.create_device_objects()
        return self

    def create_device_objects(self):
        pass

    def add_layer(self, layer: Layer):
        self.layers[layer.name] = layer
        self.add_child(layer)

    def remove_layer(self, layer: Layer):
        self.layers.pop(layer.name)
        self.remove_child(layer)

    def get_layer(self, name: str) -> Layer:
        return self.layers[name]
    
    def on_show(self):
        pass

    def on_hide(self):
        pass