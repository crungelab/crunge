from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from crunge.engine import Base, Vu
from crunge.engine.d2.renderer_2d import Renderer2D

T_Node = TypeVar("T_Node")
T_Scene = TypeVar("T_Scene")
T_Renderer = TypeVar("T_Renderer")

class Node(Base, Generic[T_Node, T_Scene, T_Renderer]):
    def __init__(self, vu: Vu = None) -> None:
        super().__init__()
        self.vu = vu
        self.scene: T_Scene = None
        self.parent: "Node[T_Node]" = None
        self.children: List["Node[T_Node]"] = []

    def clear(self):
        for child in self.children:
            child.clear()
        self.children.clear()

    def destroy(self):
        if self.parent:
            self.parent.detach(self)
        for child in self.children:
            child.destroy()
        self.clear()

    def attach(self, child: "Node[T_Node]"):
        child.parent = self
        child.scene = self.scene
        self.children.append(child)
        child.on_attached()

    def on_attached(self):
        pass

    def detach(self, child: "Node[T_Node]"):
        child.parent = None
        self.children.remove(child)
        child.on_detached()

    def on_detached(self):
        pass

    def draw(self, renderer: T_Renderer):
        if self.vu is not None:
            self.vu.draw(renderer)
        for child in self.children:
            child.draw(renderer)

    def update(self, delta_time: float):
        if self.vu is not None:
            self.vu.update(delta_time)
        for child in self.children:
            child.update(delta_time)