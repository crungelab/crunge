from ..texture import SpriteTexture
from ...d2.sprite import Sprite
from .sprite_strip import SpriteStrip
from .sprite_set import SpriteSet

class SpriteGrid(SpriteSet):
    def __init__(self, texture: SpriteTexture) -> None:
        super().__init__(texture)
        self.rows: list[SpriteStrip] = []

    def __getitem__(self, index: int) -> SpriteStrip:
        return self.rows[index]

    def add(self, row: SpriteStrip):
        self.rows.append(row)

    def get(self, index: int) -> Sprite:
        return self.rows[index]