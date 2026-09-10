from typing import TYPE_CHECKING

from ..scene_node import SceneNode

if TYPE_CHECKING:
    from .. import Scene

from .scene_layer import SceneLayer

class GraphLayer[T_Node: SceneNode](SceneLayer):
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
    def nodes(self) -> list[T_Node]:
        return self.root.children

    def _create(self) -> None:
        super()._create()
        self.root.create()

    def _enable(self) -> None:
        super()._enable()
        self.root.enable()

    def _disable(self) -> None:
        super()._disable()
        self.root.disable()

    def _destroy(self) -> None:
        super()._destroy()
        self.root.destroy()

    def _ready(self) -> None:
        super()._ready()
        self.root.ready()

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