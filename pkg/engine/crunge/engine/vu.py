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
    def current_viewport(self) -> Viewport:
        return Viewport.get_current()

    @property
    def current_renderer(self) -> Renderer:
        return Renderer.get_current()
    
    @property
    def node(self) -> T_Node:
        return self._node

    @node.setter
    def node(self, value: T_Node):
        self._node = value
        value.add_listener(self)
    
    """
    @node.setter
    def node(self, value: T_Node):
        self._node = value
        value.add_listener(self)
        # Don't rely on catching the node's next transform/model change -
        # construction order isn't guaranteed relative to the node's own
        # initial dirty pass, so a Vu attached after that pass has already
        # fired would otherwise be stuck with stale constructor defaults
        # (e.g. an identity transform) until something moves again.
        self.on_node_transform_change(value)
        if value.model is not None:
            self.on_node_model_change(value)
    """
            
    def draw(self):
        self._draw()

    def _draw(self):
        pass

    def update(self, delta_time: float):
        pass