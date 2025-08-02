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

    def __iter__(self):
        """Make Layer iterable by returning iterator over nodes"""
        return iter(self.nodes)

    def __len__(self):
        """Return the number of nodes in the layer"""
        return len(self.nodes)

    @property
    def nodes(self) -> List[T_Node]:
        return self.root.children

    def clear(self) -> None:
        self.root.clear()

    def draw(self) -> None:
        self._draw()

    def _draw(self) -> None:
        self.root.draw()

    def update(self, dt: float) -> None:
        self.root.update(dt)

    def attach(self, node: T_Node) -> None:
        self.root.attach(node)

    def detach(self, node: T_Node) -> None:
        self.root.detach(node)