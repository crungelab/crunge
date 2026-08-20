from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from ..scene_node import SceneNode, T_Node

if TYPE_CHECKING:
    from .. import Scene

from .scene_layer import SceneLayer

class GraphLayer(SceneLayer, Generic[T_Node]):
    scene: "Scene[T_Node]"

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.root: SceneNode[T_Node] = None

    def __iter__(self):
        """Make GraphLayer iterable by returning iterator over nodes"""
        return iter(self.nodes)

    def __len__(self):
        """Return the number of nodes in the GraphLayer"""
        return len(self.nodes)

    @property
    def nodes(self) -> List[T_Node]:
        return self.root.children

    def clear(self) -> None:
        self.root.clear()

    def _draw(self) -> None:
        self.root.draw()

    def update(self, dt: float) -> None:
        self.root.update(dt)

    def attach(self, node: T_Node) -> None:
        self.root.add_child(node)

    def detach(self, node: T_Node) -> None:
        self.root.remove_child(node)