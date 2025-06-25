from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from . import Base, Renderer

from .scene_node import SceneNode, T_Node

if TYPE_CHECKING:
    from .scene import Scene


class SceneLayer(Base, Generic[T_Node]):
    def __init__(self, name: str) -> None:
        super().__init__()
        self.name = name
        self.scene: Scene[T_Node] = None
        self.root: "SceneNode[T_Node]" = None

    @property
    def nodes(self):
        return self.root.children

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