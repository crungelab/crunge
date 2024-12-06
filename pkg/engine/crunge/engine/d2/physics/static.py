import math

import glm
import pymunk

from .constants import PT_STATIC
from .physics import Physics

class StaticPhysics(Physics):
    def __init__(self):
        super().__init__(PT_STATIC)

    def create_body(self, node, offset=glm.vec2()):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.node = node
        position = node.position + offset
        body.position = pymunk.Vec2d(position.x, position.y)
        body.angle = math.radians(node.angle)
        return body
