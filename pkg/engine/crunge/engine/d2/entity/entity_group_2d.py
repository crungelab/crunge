
import glm

from .entity_2d import Entity2D

class EntityGroup2D(Entity2D):
    default_vu = None

    _id_counter = 0

    def __init__(self, position: glm.vec2 = None):
        super().__init__(position)
        EntityGroup2D._id_counter += 1
        self.id = EntityGroup2D._id_counter
        self.nodes: list[Entity2D] = []

    def add_node(self, node: Entity2D):
        node.group = self
        self.nodes.append(node)
        self.add_child(node)
        return node

    def _create(self):
        super()._create()
        for node in self.nodes:
            node.gid = self.id
            self.layer.attach(node)

    def update(self, delta_time: float):
        points = [node.position for node in self.nodes]
        if points:
            centroid = glm.vec2(
                sum(point.x for point in points) / len(points),
                sum(point.y for point in points) / len(points),
            )
        else:
            centroid = glm.vec2(0, 0)
        self.position = centroid
        return super().update(delta_time)