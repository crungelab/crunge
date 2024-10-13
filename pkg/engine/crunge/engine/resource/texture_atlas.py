from typing import Dict

import glm

from ..math import Rect2i

from .texture import Texture


class TextureAtlas(Texture):
    def __init__(self, texture, rect: Rect2i):
        super().__init__(texture, rect)
        self.textures: Dict[str, Texture] = {}

    def add(self, texture: Texture):
        self.textures[texture.name] = texture

    def get(self, name: str) -> Texture:
        return self.textures[name]
