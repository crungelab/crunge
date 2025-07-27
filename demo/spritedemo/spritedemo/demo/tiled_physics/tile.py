import glm

from crunge.engine.d2.sprite import Sprite, SpriteVu

from crunge.engine.d2.entity import StaticEntity2D


class Tile(StaticEntity2D):
    def __init__(self, position: glm.vec2, sprite: Sprite) -> None:
        vu = SpriteVu(sprite)
        super().__init__(position, vu=vu, model=sprite)
