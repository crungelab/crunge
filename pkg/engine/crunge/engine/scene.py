from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from crunge.engine import Base, Vu
from crunge.engine.d2.renderer_2d import Renderer2D

from .scene_node import SceneNode

T_Node = TypeVar("T_Node")
T_Renderer = TypeVar("T_Renderer")

class Scene(Base, Generic[T_Node, T_Renderer]):
    def __init__(self) -> None:
        super().__init__()
        self.root: "SceneNode[T_Node]" = SceneNode()

    def clear(self):
        self.root.clear()

    def draw(self, renderer: T_Renderer):
        self.root.draw(renderer)

    def update(self, dt: float):
        self.root.update(dt)
