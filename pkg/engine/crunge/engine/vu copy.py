from typing import TYPE_CHECKING, TypeVar, Generic

from .chip import Chip
from .node import Node

from .viewport import Viewport
from .easel import Easel
from .renderer import Renderer

T_Node = TypeVar("T_Node", bound=Node)


class Vu(Chip[T_Node], Generic[T_Node]):
    def __init__(self) -> None:
        super().__init__()
        self._node: T_Node = None

    @property
    def current_viewport(self) -> Viewport:
        return Viewport.get_current()

    @property
    def current_easel(self) -> Easel:
        return self.current_viewport.easel if self.current_viewport else None

    @property
    def current_renderer(self) -> Renderer:
        return Renderer.get_current()

    @property
    def node(self) -> T_Node:
        return self._node

    @node.setter
    def node(self, value: T_Node):
        self._node = value
        value.transform_changed.connect(self.on_node_transform_change)
        value.model_changed.connect(self.on_node_model_change)

    def draw(self):
        self._draw()

    def _draw(self):
        pass

    def update(self, delta_time: float):
        pass

    def on_node_transform_change(self, node: T_Node) -> None:
        pass

    def on_node_model_change(self, node: T_Node) -> None:
        pass
