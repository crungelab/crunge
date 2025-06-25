from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from . import Base, Vu, Renderer

from .scene_node import SceneNode
from .scene_layer import SceneLayer

T_Node = TypeVar("T_Node")

class Scene(Base, Generic[T_Node]):
    def __init__(self) -> None:
        super().__init__()
        #self.root: "SceneNode[T_Node]" = None
        self.primary_layer: "SceneLayer[T_Node]" = None
        self.layers: List[SceneLayer[T_Node]] = []
        self.layers_by_name: Dict[str, SceneLayer[T_Node]] = {}

    '''
    @property
    def nodes(self):
        return self.primary_layer.nodes
    '''

    def _create(self):
        super()._create()
        self.create_layers()

    def create_layers(self):
        raise NotImplementedError

    def add_layer(self, layer: SceneLayer[T_Node]):
        layer.scene = self
        self.layers.append(layer)
        self.layers_by_name[layer.name] = layer
        layer.enable()
        return layer
    
    def remove_layer(self, layer: SceneLayer[T_Node]):
        self.layers.remove(layer)
        del self.layers_by_name[layer.name]
        return layer

    def get_layer(self, name: str):
        return self.layers_by_name.get(name)
    
    def clear(self):
        for layer in self.layers:
            layer.clear()

    def draw(self, renderer: Renderer):
        for layer in self.layers:
            layer.draw(renderer)

    def update(self, dt: float):
        for layer in self.layers:
            layer.update(dt)

    def attach(self, node: T_Node):
        self.primary_layer.attach(node)

    def detach(self, node: T_Node):
        self.primary_layer.detach(node)