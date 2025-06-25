from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List, Callable, Any

from .renderer import Renderer
from .base import Base
from .node import Node, NodeListener

T_Node = TypeVar("T_Node")

class Vu(Base, NodeListener, Generic[T_Node]):
    def __init__(self) -> None:
        super().__init__()
        self._node: T_Node = None

    @property
    def node(self) -> T_Node:
        return self._node
    
    @node.setter
    def node(self, value: T_Node):
        self._node = value
        value.add_listener(self)

    def draw(self, renderer: Renderer):
        pass

    def update(self, delta_time: float):
        pass