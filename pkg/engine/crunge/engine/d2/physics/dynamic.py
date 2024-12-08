import math

from loguru import logger
import glm

import pymunk

from .constants import PT_DYNAMIC, GRAVITY
from . import Physics, PhysicsEngine2D


class DynamicPhysics(Physics):
    def __init__(self, position=glm.vec2()):
        super().__init__(PT_DYNAMIC, position)

    def create_body(self, node):
        mass = node.mass
        #logger.debug(f"mass: {mass}")
        #moment = pymunk.moment_for_box(mass, (self.width, self.height))
        moment = node.geom.get_moment(node)
        #logger.debug(f"moment: {moment}")
        body = pymunk.Body(mass, moment)
        body.node = node

        position = node.position + self.position
        #logger.debug(f"position: {position}")
        body.position = pymunk.Vec2d(position.x, position.y)
        body.angle = math.radians(node.angle)
        return body

class DynamicPhysicsEngine(PhysicsEngine2D):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__(gravity=gravity, iterations=iterations)
