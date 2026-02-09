from typing import TYPE_CHECKING

from ... import Node

if TYPE_CHECKING:
    from ...vu import Vu
    from ...model import Model
    from .. import Scene


class SceneLayer(Node["SceneLayer"]):
    def __init__(self, name: str, vu: "Vu" = None, model: "Model" = None) -> None:
        super().__init__(vu=vu, model=model)
        self.name = name
        self.scene: Scene = None
        self.layers_by_name: dict[str, SceneLayer] = {}

    def add_layer(self, layer: "SceneLayer"):
        layer.scene = self
        self.add_child(layer)
        self.layers_by_name[layer.name] = layer
        # layer.enable() #redundant. enabled by add_child
        return layer

    def remove_layer(self, layer: "SceneLayer"):
        self.remove_child(layer)
        del self.layers_by_name[layer.name]
        return layer

    def get_layer(self, name: str):
        return self.layers_by_name.get(name)
