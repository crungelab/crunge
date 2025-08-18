from typing import Dict

from ...d2.sprite import Sprite

from ..texture import SpriteTexture
from .sprite_set import SpriteSet

class SpriteAtlas(SpriteSet[SpriteTexture]):
    def __init__(self, texture: SpriteTexture):
        super().__init__(texture)
        #self.sprites: list[Sprite] = []
        #self.sprite_map: Dict[str, Sprite] = {}
