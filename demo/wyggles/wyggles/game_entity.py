import math
import glm

from crunge.engine.d2 import SpriteVu
from crunge.engine.d2.entity import Entity2D
from crunge.engine.loader.sprite.sprite_loader import SpriteLoader


class GameEntity(Entity2D):
    vu_class: type[SpriteVu] | None = SpriteVu
    def __init__(self, dna=None):
        super().__init__()
        self.dna = dna
        self.kind = self.__class__.__name__
        self.mind = None
        self.body = None
        self._z = 0
        #
        self.energy = 5

    @property
    def z(self):
        return self._z

    @z.setter
    def z(self, val):
        self._z = val
        self.layer.depth_sort()

    def update(self, delta_time: float = 1 / 60):
        """
        if self.brain:
            self.brain.update(delta_time)
        """
        if self.body:
            self.position = glm.vec2(self.body.position)
            self.rotation = self.body.angle

        super().update(delta_time)

    def load_sprite(self, filename):
        self.model = SpriteLoader().load(filename)

    def _enable(self):
        super()._enable()
        pos = self.position
        if self.body != None:
            self.body.position = pos.x, pos.y


class SpriteFactory:
    def __init__(self, layer):
        self.layer = layer
