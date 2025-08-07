from typing import Dict

import glm

from crunge import wgpu

from ...d2.sprite import Sprite
from ..image import Image

from ..texture import ImageTexture
from .sprite_set import SpriteSet

class SpriteAtlas(SpriteSet[ImageTexture]):
    def __init__(self, texture: ImageTexture):
        super().__init__(texture)
        self.sprites: list[Sprite] = []
        self.sprite_map: Dict[str, Sprite] = {}
