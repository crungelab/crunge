from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

from loguru import logger

from crunge import yoga

if TYPE_CHECKING:
    from .window import Window

from .widget import Widget
from .view_layer import ViewLayer


class View(Widget):
    def __init__(self, layers: list[ViewLayer] = []) -> None:
        style = yoga.StyleBuilder().size_percent(100, 100).build()
        super().__init__(style)
        self.window: "Window" = None
        self.layers_by_name: Dict[str, ViewLayer] = {}

        for layer in layers:
            self.add_layer(layer)

    @property
    def layers(self) -> List[ViewLayer]:
        return self.children

    def _create(self):
        #logger.debug("View.create")
        super()._create()
        if not self.window:
            raise ValueError("View.window is not set")
        for layer in self.layers:
            layer.config(view=self).create()
        self.create_device_objects()
        self.create_camera()
        self.create_renderer()
        #super()._create()

    def create_device_objects(self):
        pass

    def create_camera(self):
        pass

    def create_renderer(self):
        pass

    def add_layer(self, layer: ViewLayer) -> ViewLayer:
        layer.view = self
        self.layers_by_name[layer.name] = layer
        self.attach(layer)
        self.sort_children(key=lambda child: child.priority)
        return layer

    def remove_layer(self, layer: ViewLayer):
        layer.view = None
        self.layers_by_name.pop(layer.name)
        self.detach(layer)

    def get_layer(self, name: str) -> ViewLayer:
        return self.layers_by_name[name]
