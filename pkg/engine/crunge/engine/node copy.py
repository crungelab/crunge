from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable
from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from crunge.engine import Base, Vu
from crunge.engine.d2.renderer_2d import Renderer2D

T_Dimension = TypeVar("T_Dimension")

class Node(Base, Generic[T_Dimension]):
    def __init__(self, vu: Vu = None) -> None:
        super().__init__()
        self.vu = vu
        self.scene: "Scene[T_Dimension]" = None
        self.parent: "Node[T_Dimension]" = None
        self.children: List["Node[T_Dimension]"] = []

    def clear(self):
        for child in self.children:
            child.clear()
        self.children.clear()

    def destroy(self):
        if self.parent:
            self.parent.remove_child(self)
        for child in self.children:
            child.destroy()
        self.clear()

    def add_child(self, child: "Node"):
        child.parent = self
        child.scene = self.scene
        self.children.append(child)

    def remove_child(self, child: "Node"):
        child.parent = None
        self.children.remove(child)

    def draw(self, renderer: Renderer2D):
        if self.vu is not None:
            self.vu.draw(renderer)
        for child in self.children:
            child.draw(renderer)

    def update(self, delta_time: float):
        if self.vu is not None:
            self.vu.update(delta_time)
        for child in self.children:
            child.update(delta_time)