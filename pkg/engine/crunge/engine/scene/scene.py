from typing import TYPE_CHECKING, Optional, TypeVar, Generic, Dict, List
import contextlib
from contextvars import ContextVar

from ..updater import Updater, Phase, Entry

from .scene_node import SceneNode
from .layer.graph_layer import GraphLayer
from .layer.layer_group import LayerGroup

T_Node = TypeVar("T_Node", bound=SceneNode)

current_scene: ContextVar[Optional["Scene"]] = ContextVar("current_scene", default=None)


class Scene(LayerGroup, Generic[T_Node]):
    def __init__(self, name: str) -> None:
        super().__init__(name)

    def _enable(self):
        super()._enable()
        self.make_current()
        Updater().register(self, phase=Phase.PHYSICS)

    def _disable(self):
        Updater().unregister(self)
        super()._disable()

    @property
    def primary_layer(self) -> GraphLayer[T_Node]:
        if not self.children:
            raise ValueError("No layers in the scene.")
        return self.children[0]

    def make_current(self):
        current_scene.set(self)

    @classmethod
    def get_current(cls) -> Optional["Scene"]:
        return current_scene.get()

    def attach(self, node: T_Node):
        self.primary_layer.attach(node)

    def detach(self, node: T_Node):
        self.primary_layer.detach(node)
