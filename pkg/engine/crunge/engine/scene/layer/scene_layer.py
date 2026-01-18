from typing import TYPE_CHECKING

from ... import Node

if TYPE_CHECKING:
    from .. import Scene


class SceneLayer(Node["SceneLayer"]):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.scene: Scene = None
        self.layers_by_name: dict[str, SceneLayer] = {}

    def add_layer(self, layer: "SceneLayer"):
        layer.scene = self
        #self.layers.append(layer)
        self.add_child(layer)
        self.layers_by_name[layer.name] = layer
        layer.enable()
        return layer
    
    def remove_layer(self, layer: "SceneLayer"):
        #self.layers.remove(layer)
        self.remove_child(layer)
        del self.layers_by_name[layer.name]
        return layer

    def get_layer(self, name: str):
        return self.layers_by_name.get(name)

    '''
    def clear(self) -> None:
        pass
    
    def draw(self) -> None:
        self._draw()

    def _draw(self) -> None:
        pass

    def update(self, dt: float) -> None:
        pass
    '''