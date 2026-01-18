from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from ... import Base

from .scene_layer import SceneLayer


class GroupLayer(SceneLayer):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.layers: List[SceneLayer] = []
        self.layers_by_name: Dict[str, SceneLayer] = {}
    
    def add_layer(self, layer: SceneLayer):
        layer.scene = self
        self.layers.append(layer)
        self.layers_by_name[layer.name] = layer
        layer.enable()
        return layer
    
    def remove_layer(self, layer: SceneLayer):
        self.layers.remove(layer)
        del self.layers_by_name[layer.name]
        return layer

    def get_layer(self, name: str):
        return self.layers_by_name.get(name)

    def clear(self):
        for layer in self.layers:
            layer.clear()

    def _draw(self):
        for layer in self.layers:
            layer.draw()

    def update(self, dt: float):
        for layer in self.layers:
            layer.update(dt)
