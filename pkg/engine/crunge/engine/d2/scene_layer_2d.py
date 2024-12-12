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

    def __str__(self):
        #return f"SceneLayer2D(name={self.name}, bounds={self.bounds})"
        return f"SceneLayer2D(name={self.name})"
    
    def __repr__(self):
        return str(self)

    def query_intersection(self, bounds: Bounds2):
        result:list[Node2D] = []
        for node in self.nodes:
            if node.bounds.intersects(bounds):
                result.append(node)
        return result