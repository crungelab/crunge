import glm

from . import Texture
from ...d2.sprite import Sprite

class SpriteStrip(Texture):
    def __init__(self, texture, size: glm.ivec2):
        super().__init__(texture, size)
        self.sprites: list[Sprite] = []

    def __getitem__(self, index: int) -> Sprite:
        return self.sprites[index]

    def add(self, sprite: Sprite):
        self.sprites.append(sprite)

    def get(self, index: int) -> Sprite:
        return self.sprites[index]
