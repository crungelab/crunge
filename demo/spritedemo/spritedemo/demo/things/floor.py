import glm

from ...sprite import Sprite
#from ...node_2d import Node2D
from ...model_2d import StaticModel2D
from ...texture_kit import TextureKit
from ...resource_kit import ResourceKit
from ...geom import BoxGeom

class Floor(StaticModel2D):
    def __init__(self, position: glm.vec2, size: glm.vec2) -> None:
        super().__init__(geom=BoxGeom)
        self.position = position
        self.size = size
