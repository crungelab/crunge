from loguru import logger

import glm

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.vu_2d import Vu2D


class Entity2D(Node2D):
    def __init__(
        self,
        position=glm.vec2(),
        size=glm.vec2(1.0),
        scale=glm.vec2(1.0),
        vu: Vu2D = None,
        model=None,
        brain=None,
    ):
        super().__init__(position, size, scale, vu, model)
        self.layer = None
        self.brain = brain
        #logger.debug(f"Entity2D: {self}")

    def _create(self):
        super()._create()
        if self.vu is not None and self.layer is not None:
            self.layer.add_sprite(self.vu)

    def update(self, delta_time: float):
        super().update(delta_time)
        self.update_brain(delta_time)

    def update_brain(self, delta_time):
        if self.brain:
            self.brain.update(delta_time)


class EntityGroup2D(Entity2D):
    id_counter = 1

    def __init__(self, position=glm.vec2()):
        super().__init__(position)
        self.id_counter += 1
        self.id = self.id_counter
        self.models = []

    def add_model(self, model):
        # model.parent = self
        self.models.append(model)
        return model

    def _create(self):
        super()._create()
        for model in self.models:
            model.gid = self.id
            self.layer.add_model(model)