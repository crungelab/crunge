from enum import Enum

import glm

from crunge.engine.base import Base

from .constants import *
from .world import PhysicsWorld2D

class MotionState(Enum):
    GROUNDED = 0
    JUMPING = 1
    CLIMBING = 2
    FALLING = 3
    MOUNTED = 4


class Physics(Base):
    def __init__(self, kind, position=glm.vec2()):
        self.kind = kind
        self.position = position

    @property
    def world(self) -> PhysicsWorld2D:
        return PhysicsWorld2D.get_current()

class GroupPhysics(Physics):
    def __init__(self, kind=PT_GROUP):
        super().__init__(kind)

    def create():
        pass

    def update(self, model, delta_time=1 / 60.0):
        pass

    def create_body(self, model, offset=None):
        pass
