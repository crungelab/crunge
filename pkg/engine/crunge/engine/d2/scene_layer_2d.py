from loguru import logger
import glm

from ..scene_layer import SceneLayer
from .node_2d import Node2D

class SceneLayer2D(SceneLayer[Node2D]):
    def __init__(self, name: str, size=glm.ivec2()) -> None:
        super().__init__(name)
        self.size = size
        self.root = Node2D()
        self.root.layer = self

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