from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List

from loguru import logger

from crunge.engine import Vu

from ..node import Node, T_Node
from .layer.scene_layer import SceneLayer

T_Layer = TypeVar("T_Layer", bound=SceneLayer)


class SceneNode(Node[T_Node], Generic[T_Node, T_Layer]):
    def __init__(self, vu: Vu = None, model=None) -> None:
        super().__init__(vu, model)
        self.layer: T_Layer = None

    @property
    def scene(self):
        return self.layer.scene

    def add_child(self, child: "SceneNode[T_Node, T_Layer]"):
        # logger.debug(f"Attaching child: {child} to parent: {self} with layer: {self.layer}")
        child.layer = self.layer
        return super().add_child(child)
