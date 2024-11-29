from loguru import logger
import glm

from ..scene import Scene
from .node_2d import Node2D
from .scene_layer_2d import SceneLayer2D

class Scene2D(Scene[Node2D]):
    def __init__(self) -> None:
        super().__init__()

    def create_layers(self):
        self.primary_layer = SceneLayer2D('primary')
        self.primary_layer.scene = self
        self.add_layer(self.primary_layer)
