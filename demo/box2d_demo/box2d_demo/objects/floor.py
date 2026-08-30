import glm

from crunge.engine.d2 import Node2D
from crunge.engine.d2.physics import StaticPhysics
from crunge.engine.d2.physics.geom import BoxGeom

class Floor(Node2D):
    def __init__(self, position: glm.vec2, scale: glm.vec2) -> None:
        super().__init__(position, scale=scale)

    def _seat(self) -> None:
        super()._seat()
        self.add(StaticPhysics(BoxGeom()))
