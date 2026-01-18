from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from .scene_node import SceneNode
from .layer.graph_layer import GraphLayer
from .layer.group_layer import GroupLayer

T_Node = TypeVar("T_Node", bound=SceneNode)


class Scene(GroupLayer, Generic[T_Node]):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        #self.primary_layer: "SceneLayer[T_Node]" = None

    @property
    def primary_layer(self) -> GraphLayer[T_Node]:
        if not self.layers:
            raise ValueError("No layers in the scene.")
        return self.layers[0]
    
    def attach(self, node: T_Node):
        self.primary_layer.attach(node)

    def detach(self, node: T_Node):
        self.primary_layer.detach(node)