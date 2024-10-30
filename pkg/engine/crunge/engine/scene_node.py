from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from crunge.engine import Vu

from .node import Node, T_Node, T_Vu, T_Renderer

T_Scene = TypeVar("T_Scene")

class SceneNode(Node[T_Node, T_Vu, T_Renderer], Generic[T_Node, T_Vu, T_Renderer, T_Scene]):
    def __init__(self, vu: Vu = None) -> None:
        super().__init__(vu)
        self.scene: T_Scene = None

    def attach(self, child: "SceneNode[T_Node]"):
        child.scene = self.scene
        super().attach(child)