import math

from loguru import logger
import glm

from crunge import box2d

from .constants import PT_DYNAMIC, GRAVITY
from . import Physics


class DynamicPhysics(Physics):
    def __init__(self, position=glm.vec2()):
        super().__init__(PT_DYNAMIC, position)

    def create_body(self, node):
        logger.debug(f"Creating body for node: {node}")
        position = node.position + self.position
        body_position = box2d.Vec2(position.x, position.y)
        rotation = box2d.make_rot(node.angle)

        body_def = box2d.BodyDef(type=box2d.BodyType.DYNAMIC_BODY, position=body_position, rotation=rotation)
        body = self.world.create_body(body_def)
        body.user_data = node

        return body
