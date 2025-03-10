from loguru import logger

import glm

from crunge.engine.d2.node_2d import Node2D
from crunge.engine.d2.vu_2d import Vu2D


class Entity2D(Node2D):
    def __init__(
        self,
        position=glm.vec2(),
        rotation=0.0,
        scale=glm.vec2(1.0),
        vu: Vu2D = None,
        model=None,
        brain=None,
    ):
        super().__init__(position, rotation, scale, vu, model)
        self.layer = None
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

    '''
    def _create(self):
        super()._create()
        if self.vu is not None and self.layer is not None:
            self.layer.add_sprite(self.vu)
    '''

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
        self.nodes = []

    def add_node(self, node):
        node.group = self
        self.nodes.append(node)
        return node

    def _create(self):
        super()._create()
        for node in self.nodes:
            node.gid = self.id
            self.layer.attach(node)
