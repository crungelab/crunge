from typing import Dict

import glm

from .. import RectI

from .texture import Texture


class TextureAtlas(Texture):
    def __init__(self, rect: RectI, texture):
        super().__init__(rect, texture)
        self.textures: Dict[str, Texture] = {}

    def add(self, texture: Texture):
        self.textures[texture.name] = texture

    def get(self, name: str) -> Texture:
        return self.textures[name]
