from loguru import logger

import glm

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.vu_2d import Vu2D

from .brain import EntityBrain

class Entity2D(Node2D):
    def __init__(
        self,
        position=glm.vec2(),
        rotation=0.0,
        scale=glm.vec2(1.0),
        model=None,
        brain: EntityBrain = None,
    ):
        super().__init__(position, rotation, scale, model=model)
        self._brain = None
        if brain is not None:
            self.brain = brain
        #logger.debug(f"Entity2D: {self}")

    @property
    def brain(self):
        return self._brain
    
    @brain.setter
    def brain(self, value):
        self._brain = value
        self._brain.node = self
        value.enable()

    def update(self, delta_time: float):
        super().update(delta_time)
        self.update_brain(delta_time)

    def update_brain(self, delta_time):
        if self.brain:
            self.brain.update(delta_time)
