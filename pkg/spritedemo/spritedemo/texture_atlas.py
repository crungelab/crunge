from typing import Dict

from .texture import Texture


class TextureAtlas(Texture):
    def __init__(self, texture, width: int, height: int):
        super().__init__(texture, 0, 0, width, height)
        self.textures: Dict[str, Texture] = {}

    def add(self, name: str, texture: Texture):
        self.textures[name] = texture

    def get(self, name: str) -> Texture:
        return self.textures[name]
