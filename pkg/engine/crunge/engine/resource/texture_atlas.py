from typing import Dict

import glm

from crunge import wgpu

from ..math import Rect2i

from .texture import Texture


class TextureAtlas(Texture):
    def __init__(self, texture: wgpu.Texture, rect: Rect2i):
        super().__init__(texture, rect)
        self.textures: list[Texture] = []
        self.texture_map: Dict[str, Texture] = {}

    def __getitem__(self, index: int) -> Texture:
        return self.textures[index]
    
    def add(self, texture: Texture):
        self.textures.append(texture)
        self.texture_map[texture.name] = texture

    def get(self, name: str) -> Texture:
        return self.texture_map[name]

'''
class TextureAtlas(Texture):
    def __init__(self, texture, rect: Rect2i):
        super().__init__(texture, rect)
        self.textures: Dict[str, Texture] = {}

    def add(self, texture: Texture):
        self.textures[texture.name] = texture

    def get(self, name: str) -> Texture:
        return self.textures[name]
'''