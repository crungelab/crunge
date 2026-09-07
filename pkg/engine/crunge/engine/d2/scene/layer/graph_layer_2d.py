import random

from loguru import logger
import glm

from ....math import Bounds2

from ....scene.layer.graph_layer import GraphLayer
from ...node_2d import Node2D

class GraphLayer2D(GraphLayer[Node2D]):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        #self.bounds = Bounds2()
        self.root = Node2D()
        self.root.layer = self

    def __str__(self):
        return f"GraphLayer2D(name={self.name})"
    
    def __repr__(self):
        return str(self)

    @property
    def bounds(self) -> Bounds2:
        return self.scene.bounds

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
            if node.global_bounds.intersects(bounds):
                result.append(node)
        return result

    def materialize_random_from_center(self, node: Node2D):
        world_right = self.bounds.max.x
        world_top = self.bounds.max.y
        halfMaxX = world_right / 2
        halfMaxY = world_top / 2
        diameter = world_top
        radius = diameter / 2

        position = glm.vec2(
            (halfMaxX - radius) + (random.random() * diameter),
            (halfMaxY - radius) + (random.random() * diameter),
        )

        logger.debug(f"Materializing node {node} at position {position} within bounds {self.bounds}")

        node.position = position


        self.attach(node)
