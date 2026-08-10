from ..texture import SpriteTexture
from .sprite_set import SpriteSet


class SpriteAtlas(SpriteSet[SpriteTexture]):
    def __init__(self, texture: SpriteTexture):
        super().__init__(texture)
