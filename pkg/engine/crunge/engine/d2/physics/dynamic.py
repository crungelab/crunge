import math

from loguru import logger

import pymunk
from pymunk.vec2d import Vec2d

from .constants import PT_DYNAMIC, GRAVITY
from . import Physics, PhysicsMeta, PhysicsEngine
from .draw_options import DrawOptions

class DynamicPhysics(Physics, metaclass=PhysicsMeta):
    def __init__(self):
        super().__init__(PT_DYNAMIC)

    def update(self, model, delta_time=1/60.0):
        pass

    def create_body(self, model, offset=None):
        mass = model.mass
        #logger.debug(f"mass: {mass}")
        #moment = pymunk.moment_for_box(mass, (self.width, self.height))
        moment = model.geom.get_moment(model)
        #logger.debug(f"moment: {moment}")
        body = pymunk.Body(mass, moment)
        body.model = model

        if offset:
            #print('offset', offset)
            position = (model.position.x + offset[0], model.position.y + offset[1])

        else:
            position = model.position
        #logger.debug(f"position: {position}")
        body.position = Vec2d(position.x, position.y)
        body.angle = math.radians(model.angle)
        return body

class DynamicPhysicsEngine(PhysicsEngine):
    def __init__(self, gravity=GRAVITY, iterations=35, draw_options: DrawOptions = None):
        super().__init__(gravity=gravity, iterations=iterations, draw_options=draw_options)