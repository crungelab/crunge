import glm

from ...base import Base

from .constants import *


class Physics(Base):
    def __init__(self, kind, position=glm.vec2()):
        self.kind = kind
        self.position = position


class GroupPhysics(Physics):
    def __init__(self, kind=PT_GROUP):
        super().__init__(kind)

    def create():
        pass

    def update(self, model, delta_time=1 / 60.0):
        pass

    def create_body(self, model, offset=None):
        pass
