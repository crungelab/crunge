from loguru import logger
import glm

from ..math import Bounds2

from ..scene_layer import SceneLayer
from .node_2d import Node2D

class SceneLayer2D(SceneLayer[Node2D]):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.bounds = Bounds2()
        self.root = Node2D()
        self.root.layer = self

    '''
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

    @property
    def top(self):
        return self.size.y
    
    @property
    def right(self):
        return self.size.x
    
    @property
    def bottom(self):
        return 0
    
    @property
    def left(self):
        return 0
    '''

    def query_intersection(self, bounds: Bounds2):
        result:list[Node2D] = []
        for node in self.nodes:
            if node.bounds.intersects(bounds):
                result.append(node)
        return result