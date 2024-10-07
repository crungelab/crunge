from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .window import Window

from loguru import logger
import glm

from .widget import Widget
from .view_layer import ViewLayer

class View(Widget):
    def __init__(self, size=glm.ivec2(), layers: list[ViewLayer]=[]) -> None:
        super().__init__(size)
        self.window: "Window" = None
        #self.layers: list[ViewLayer] = []
        self.layers_by_name: Dict[str, ViewLayer] = {}

        for layer in layers:
            self.add_layer(layer)

    @property
    def layers(self) -> List[ViewLayer]:
        return self.children
    
    def set_window(self, window: "Window"):
        self.window = window
        return self

    def on_size(self):
        super().on_size()
        for layer in self.layers:
            layer.size = self.size

    '''
    def resize(self, size: glm.ivec2):
        super().resize(size)
        for layer in self.layers:
            layer.resize(size)
    '''

    def create(self, window: "Window"):
        self._create(window)
        self.on_create()
        return self

    def _create(self, window: "Window"):
        logger.debug("View.create")
        super()._create()
        self.window = window
        self.size = window.size
        for layer in self.layers:
            layer.create(self)
        self.create_device_objects()
        return self

    def create_device_objects(self):
        pass

    def add_layer(self, layer: ViewLayer):
        layer.view = self
        self.layers_by_name[layer.name] = layer
        self.add_child(layer)
        self.sort_children(key=lambda child: child.priority)

    def remove_layer(self, layer: ViewLayer):
        layer.view = None
        self.layers_by_name.pop(layer.name)
        self.remove_child(layer)
        
    def get_layer(self, name: str) -> ViewLayer:
        return self.layers_by_name[name]
    
    '''
    def on_show(self):
        pass

    def on_hide(self):
        pass
    '''