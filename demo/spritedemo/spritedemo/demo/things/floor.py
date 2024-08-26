import glm

from crunge.engine.d2.sprite import Sprite
from crunge.engine.resource.texture_kit import TextureKit
from crunge.engine.resource.resource_kit import ResourceKit

from ...model_2d import StaticModel2D
from ...geom import BoxGeom

class Floor(StaticModel2D):
    def __init__(self, position: glm.vec2, size: glm.vec2) -> None:
        super().__init__(geom=BoxGeom)
        self.position = position
        self.size = size
