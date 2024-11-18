from loguru import logger

import math
import glm
import pymunk

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.vu_2d import Vu2D

#from .constants import *
#from . import globals
#from . import physics
#from .physics import geom


class Entity2D(Node2D):
    def __init__(
        self,
        position=glm.vec2(),
        size=glm.vec2(1.0),
        scale=glm.vec2(1.0),
        vu: Vu2D = None,
        brain=None,
    ):
        super().__init__(position, size, scale, vu)
        self.layer = None
        self.brain = brain

    def update(self, delta_time: float):
        super().update(delta_time)
        self.update_brain(delta_time)
        #self.update_physics(delta_time)

    def update_brain(self, delta_time):
        if self.brain:
            self.brain.update(delta_time)

    def update_physics(self, delta_time):
        pass


class EntityGroup2D(Entity2D):
    id_counter = 1

    def __init__(self, position=(0, 0)):
        super().__init__(position)
        self.id_counter += 1
        self.id = self.id_counter
        self.models = []

    def add_model(self, model):
        model.parent = self
        self.models.append(model)
        return model

    def _create(self):
        super()._create()
        for model in self.models:
            model.gid = self.id
            self.layer.add_model(model)
