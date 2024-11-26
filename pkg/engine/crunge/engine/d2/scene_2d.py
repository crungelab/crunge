from loguru import logger
import glm

from ..scene import Scene
from .node_2d import Node2D
from .scene_layer_2d import SceneLayer2D

class Scene2D(Scene[Node2D]):
    def __init__(self, size=glm.vec2()) -> None:
        super().__init__()
        self.size = size

    def create_layers(self):
        self.primary_layer = SceneLayer2D('primary', self.size)
        self.primary_layer.scene = self
        self.add_layer(self.primary_layer)

    @property
    def width(self):
        return self.size.x
    
    @width.setter
    def width(self, value):
        self.size.x = value

    @property
    def height(self):
        return self.size.y
    
    @height.setter
    def height(self, value):
        self.size.y = value