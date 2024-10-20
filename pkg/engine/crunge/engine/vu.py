from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List, Callable, Any

from .renderer import Renderer
from .base import Base


T_Node = TypeVar("T_Node")

class Vu(Base, Generic[T_Node]):
    def __init__(self) -> None:
        super().__init__()
        self.node: T_Node = None

    def pre_draw(self, renderer: Renderer):
        pass

    def draw(self, renderer: Renderer):
        pass

    def post_draw(self, renderer: Renderer):
        pass

    def update(self, delta_time: float):
        pass