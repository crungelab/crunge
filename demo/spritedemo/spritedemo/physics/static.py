import math

import pymunk

from ..constants import *
from .physics import Physics, PhysicsMeta

class StaticPhysics(Physics, metaclass=PhysicsMeta):
    def __init__(self):
        super().__init__(PT_STATIC)

    def create():
        pass

    def update(self, model, delta_time=1/60.0):
        pass

    def create_body(self, model, offset=None):
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.model = model
        position = model.position
        body.position = pymunk.Vec2d(position.x, position.y)
        body.angle = math.radians(model.angle)
        return body
