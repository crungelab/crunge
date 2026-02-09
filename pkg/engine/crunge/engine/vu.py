from typing import TYPE_CHECKING, TypeVar, Generic

from .base import Base
from .node import Node, NodeListener

from .viewport import Viewport
from .renderer import Renderer

T_Node = TypeVar("T_Node", bound=Node)

class Vu(Base, NodeListener, Generic[T_Node]):
    def __init__(self) -> None:
        super().__init__()
        self._node: T_Node = None

    @property
    def viewport(self) -> Viewport:
        return Viewport.get_current()

    @property
    def renderer(self) -> Renderer:
        return Renderer.get_current()
    
    @property
    def node(self) -> T_Node:
        return self._node
    
    @node.setter
    def node(self, value: T_Node):
        self._node = value
        value.add_listener(self)

    def draw(self):
        self._draw()

    def _draw(self):
        pass

    def render(self):
        self._render()

    def _render(self):
        self._draw()

    def update(self, delta_time: float):
        pass