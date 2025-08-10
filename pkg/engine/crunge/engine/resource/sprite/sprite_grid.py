import glm

from ..texture import SpriteTexture
from ...d2.sprite import Sprite
from .sprite_strip import SpriteStrip


class SpriteGrid(SpriteTexture):
    def __init__(self, texture, size: glm.ivec2):
        super().__init__(texture, size)
        self.rows: list[SpriteStrip] = []

    def __getitem__(self, index: int) -> SpriteStrip:
        return self.rows[index]

    def add(self, row: SpriteStrip):
        self.rows.append(row)

    def get(self, index: int) -> Sprite:
        return self.rows[index]
