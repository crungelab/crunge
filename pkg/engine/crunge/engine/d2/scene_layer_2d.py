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

    def depth_sort(self):
        nodes = self.nodes
        has_swapped = True
        while(has_swapped):
            has_swapped = False
            for i in range(len(nodes) - 1):
                if nodes[i].z > nodes[i+1].z:
                    #self.swap(i, i+1)
                    nodes[i], nodes[i+1] = nodes[i+1], nodes[i]
                    has_swapped = True

    def query_intersection(self, bounds: Bounds2):
        result:list[Node2D] = []
        for node in self.nodes:
            if node.bounds.intersects(bounds):
                result.append(node)
        return result