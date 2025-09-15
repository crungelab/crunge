import glm

from ..texture import SpriteTexture
from ...d2.sprite import Sprite
from .sprite_set import SpriteSet

class SpriteStrip(SpriteSet):
    def __init__(self, texture):
        super().__init__(texture)
        self.sprites: list[Sprite] = []

    def __getitem__(self, index: int) -> Sprite:
        return self.sprites[index]

    def add(self, sprite: Sprite):
        self.sprites.append(sprite)

    def get(self, index: int) -> Sprite:
        return self.sprites[index]
