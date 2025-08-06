from typing import Dict, List

import glm

from crunge import wgpu

from ...d2.sprite import Sprite
from ..image import Image

from .image_texture_array import ImageTextureArray


class SpriteArray(ImageTextureArray):
    def __init__(self, texture: wgpu.Texture, size: glm.ivec2, images: List[Image]):
        super().__init__(texture, size, images)
        self.sprites: list[Sprite] = []
        self.sprite_map: Dict[str, Sprite] = {}

    def __getitem__(self, index: int) -> Sprite:
        return self.sprites[index]
    
    def add(self, sprite: Sprite):
        self.sprites.append(sprite)
        self.sprite_map[sprite.name] = sprite

    def get(self, name: str) -> Sprite:
        return self.sprite_map[name]
