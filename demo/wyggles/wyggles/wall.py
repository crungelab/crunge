from crunge.engine.d2.entity import StaticEntity2D
from crunge.engine.d2.physics import BoxGeom
import glm

class Wall(StaticEntity2D):
    def __init__(self, left: float, bottom: float, right: float, top: float):
        width = right - left
        height = top - bottom
        position = glm.vec2(left + width / 2, bottom + height / 2)
        super().__init__(position, scale=glm.vec2(width, height), geom=BoxGeom())
