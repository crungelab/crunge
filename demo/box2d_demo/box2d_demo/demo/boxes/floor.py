import glm

from box2d_demo.entity import StaticEntity2D
from box2d_demo.physics.geom import BoxGeom

class Floor(StaticEntity2D):
    def __init__(self, position: glm.vec2, scale: glm.vec2) -> None:
        super().__init__(position, scale=scale, geom=BoxGeom())
