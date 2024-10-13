from typing import Dict

import glm

from ..math import Rect2i

from .texture import Texture


class TextureStrip(Texture):
    def __init__(self, texture, rect: Rect2i):
        super().__init__(texture, rect)
        self.textures: list[Texture] = []

    def add(self, texture: Texture):
        self.textures.append(texture)

    def get(self, index: int) -> Texture:
        return self.textures[index]
