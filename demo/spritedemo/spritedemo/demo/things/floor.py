import glm

from crunge.engine.d2.physics import BoxGeom
from crunge.engine.d2.entity import StaticEntity2D

class Floor(StaticEntity2D):
    def __init__(self, position: glm.vec2, size: glm.vec2) -> None:
        super().__init__(position, size, geom=BoxGeom)
