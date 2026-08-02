import glm

from crunge.engine.d2.entity import StaticEntity2D
from crunge.engine.d2.physics.geom import BoxGeom

class Floor(StaticEntity2D):
    def __init__(self, position: glm.vec2, scale: glm.vec2) -> None:
        super().__init__(position, scale=scale, geom=BoxGeom())
