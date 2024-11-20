import glm

from crunge.engine.d2.sprite import Sprite, SpriteVu
from crunge.engine.d2.entity import DynamicEntity2D


class Thing(DynamicEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        #self.sprite = sprite
        vu = SpriteVu(sprite).create()
        scale = glm.vec2(.25, .25)
        super().__init__(position, scale=scale, vu=vu, model=sprite)
