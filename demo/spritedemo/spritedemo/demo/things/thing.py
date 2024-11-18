import glm

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.resource import Texture
from ...model_2d import DynamicModel2D
from ...geom import BoxGeom


class Thing(DynamicModel2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        self.sprite = sprite
        vu = SpriteVu(sprite).create()
        scale = glm.vec2(.25, .25)
        super().__init__(position, scale=scale, vu=vu)
