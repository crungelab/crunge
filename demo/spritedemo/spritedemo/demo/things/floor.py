import glm

from ...model_2d import StaticModel2D
from ...geom import BoxGeom

class Floor(StaticModel2D):
    def __init__(self, position: glm.vec2, size: glm.vec2) -> None:
        super().__init__(position, size, geom=BoxGeom)
