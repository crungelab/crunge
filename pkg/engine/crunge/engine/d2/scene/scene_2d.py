from typing import Optional

from loguru import logger

from ...math import Bounds2
from ...scene import Scene, current_scene

from ..node_2d import Node2D
from .layer.graph_layer_2d import GraphLayer2D


class Scene2D(Scene[Node2D]):
    def __init__(self, name: str="Scene2D") -> None:
        super().__init__(name)
        self.bounds = Bounds2()

    @property
    def primary_layer(self) -> GraphLayer2D:
        if not self.children:
            self.create_default_layer()
        return self.children[0]

    @classmethod
    def get_current(cls) -> Optional["Scene2D"]:
        return current_scene.get()

    def create_default_layer(self) -> None:
        """Create and return the default primary layer for the scene."""
        layer = GraphLayer2D("primary")
        self.add_layer(layer)
