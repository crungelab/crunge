import math

import glm
from crunge import box2d
from crunge.core.utils import as_capsule

from .constants import PT_STATIC
from .physics import Physics

class StaticPhysics(Physics):
    def __init__(self, position=glm.vec2()):
        super().__init__(PT_STATIC, position)

    def create_body(self, node):
        position = node.position + self.position
        body_position = box2d.Vec2(position.x, position.y)
        body_angle = math.radians(node.angle)

        body_def = box2d.BodyDef(type=box2d.BodyType.STATIC_BODY, position=body_position, angle=body_angle)
        body = self.world.create_body(body_def)
        body.user_data = node

        return body
