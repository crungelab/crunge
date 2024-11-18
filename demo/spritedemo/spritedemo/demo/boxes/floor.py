import glm

from crunge.engine.d2.physics_entity_2d import StaticEntity2D
from crunge.engine.d2.physics.geom import BoxGeom

class Floor(StaticEntity2D):
    def __init__(self, position: glm.vec2, size: glm.vec2) -> None:
        super().__init__(position, size, geom=BoxGeom)
