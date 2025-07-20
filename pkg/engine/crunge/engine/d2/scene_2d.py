from loguru import logger
import glm

from ..math import Bounds2
from ..scene import Scene
from .node_2d import Node2D
from .scene_layer_2d import SceneLayer2D

class Scene2D(Scene[Node2D]):
    def __init__(self) -> None:
        super().__init__()
        self.bounds = Bounds2()

    @property
    def primary_layer(self) -> SceneLayer2D:
        if not self.layers:
            #raise ValueError("No layers in the scene.")
            self.create_default_layer()
        return self.layers[0]
    
    def create_default_layer(self) -> None:
        """Create and return the default primary layer for the scene."""
        layer = SceneLayer2D('primary')
        self.add_layer(layer)

    '''
    def create_layers(self):
        self.primary_layer = SceneLayer2D('primary')
        self.add_layer(self.primary_layer)
    '''