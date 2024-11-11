from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from . import Base, Vu, Renderer

from .scene_node import SceneNode

T_Node = TypeVar("T_Node")

class Scene(Base, Generic[T_Node]):
    def __init__(self) -> None:
        super().__init__()
        #self.root: "SceneNode[T_Node]" = SceneNode()
        self.root: "SceneNode[T_Node]" = None

    def clear(self):
        self.root.clear()

    def draw(self, renderer: Renderer):
        self.root.draw(renderer)

    def update(self, dt: float):
        self.root.update(dt)

    def attach(self, node: T_Node):
        self.root.attach(node)

    def detach(self, node: T_Node):
        self.root.detach(node)