import math

import pymunk

from .constants import PT_STATIC
from .physics import Physics, PhysicsMeta

class StaticPhysics(Physics, metaclass=PhysicsMeta):
    def __init__(self):
        super().__init__(PT_STATIC)

    def create():
        pass

    def update(self, model, delta_time=1/60.0):
        pass

    def create_body(self, node, offset=None):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.node = node
        position = node.position
        body.position = pymunk.Vec2d(position.x, position.y)
        body.angle = math.radians(node.angle)
        return body
