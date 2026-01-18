from loguru import logger

from ..math import Bounds2

from ..scene.layer.graph_layer import GraphLayer
from .node_2d import Node2D

class GraphLayer2D(GraphLayer[Node2D]):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.bounds = Bounds2()
        self.root = Node2D()
        self.root.layer = self

    def __str__(self):
        #return f"GraphLayer2D(name={self.name}, bounds={self.bounds})"
        return f"GraphLayer2D(name={self.name})"
    
    def __repr__(self):
        return str(self)

    def depth_sort(self):
        nodes = self.nodes
        has_swapped = True
        while(has_swapped):
            has_swapped = False
            for i in range(len(nodes) - 1):
                if nodes[i].z > nodes[i+1].z:
                    nodes[i], nodes[i+1] = nodes[i+1], nodes[i]
                    has_swapped = True

    def query_intersection(self, bounds: Bounds2):
        result:list[Node2D] = []
        for node in self.nodes:
            if node.bounds.intersects(bounds):
                result.append(node)
        return result