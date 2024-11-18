from typing import Dict

import glm

from crunge import wgpu

from ...d2.sprite import Sprite
from ..image import Image

from . import ImageTexture


class SpriteAtlas(ImageTexture):
    def __init__(self, texture: wgpu.Texture, size: glm.ivec2, image: Image):
        super().__init__(texture, size, image)
        self.sprites: list[Sprite] = []
        self.sprite_map: Dict[str, Sprite] = {}

    def __getitem__(self, index: int) -> Sprite:
        return self.sprites[index]
    
    def add(self, sprite: Sprite):
        self.sprites.append(sprite)
        self.sprite_map[sprite.name] = sprite

    def get(self, name: str) -> Sprite:
        return self.sprite_map[name]
