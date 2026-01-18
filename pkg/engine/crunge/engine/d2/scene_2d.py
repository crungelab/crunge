from loguru import logger

from ..math import Bounds2
from ..scene import Scene

from .node_2d import Node2D
from .graph_layer_2d import GraphLayer2D

class Scene2D(Scene[Node2D]):
    def __init__(self) -> None:
        super().__init__("Scene2D")
        self.bounds = Bounds2()

    @property
    def primary_layer(self) -> GraphLayer2D:
        if not self.children:
            self.create_default_layer()
        return self.children[0]

    '''
    @property
    def bounds(self) -> Bounds2:
        return self.primary_layer.bounds
    '''

    def create_default_layer(self) -> None:
        """Create and return the default primary layer for the scene."""
        layer = GraphLayer2D('primary')
        self.add_layer(layer)
