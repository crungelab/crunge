import math

from loguru import logger
import glm

import pymunk

from .constants import PT_DYNAMIC, GRAVITY
#from . import Physics, PhysicsMeta, PhysicsEngine2D
from . import Physics, PhysicsEngine2D
from .draw_options import DrawOptions

#class DynamicPhysics(Physics, metaclass=PhysicsMeta):
class DynamicPhysics(Physics):
    def __init__(self):
        super().__init__(PT_DYNAMIC)

    def create_body(self, node, offset=glm.vec2()):
        mass = node.mass
        #logger.debug(f"mass: {mass}")
        #moment = pymunk.moment_for_box(mass, (self.width, self.height))
        moment = node.geom.get_moment(node)
        #logger.debug(f"moment: {moment}")
        body = pymunk.Body(mass, moment)
        body.node = node

        position = node.position + offset
        #logger.debug(f"position: {position}")
        body.position = pymunk.Vec2d(position.x, position.y)
        body.angle = math.radians(node.angle)
        return body

class DynamicPhysicsEngine(PhysicsEngine2D):
    def __init__(self, gravity=GRAVITY, iterations=35):
        super().__init__(gravity=gravity, iterations=iterations)
