import math

from loguru import logger
import glm
from crunge import box2d

from .constants import *
from . import Physics, PhysicsWorld2D
#from .collision import CollisionHandler
from .physics import MotionState


class KinematicPhysics(Physics):
    def __init__(self, position=glm.vec2()):
        super().__init__(PT_KINEMATIC, position)

    def create_body(self, node):
        logger.debug(f"Creating body for node: {node}")
        position = node.position + self.position
        body_position = box2d.Vec2(position.x, position.y)
        rotation = box2d.make_rot(node.angle)

        body_def = box2d.BodyDef(type=box2d.BodyType.KINEMATIC_BODY, position=body_position, rotation=rotation)
        body = self.world.create_body(body_def)
        body.user_data = node

        return body
