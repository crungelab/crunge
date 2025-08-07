from typing import Dict
from typing import TypeVar, Generic



import glm

from crunge import wgpu

from ...d2.sprite import Sprite

from ..resource import Resource
from ..image import Image

from ..texture import ImageTexture


T_Texture = TypeVar("T_Texture", bound=ImageTexture)

class SpriteSet(Resource, Generic[T_Texture]):
    def __init__(self, texture: T_Texture | None = None) -> None:
        super().__init__()
        self.texture: T_Texture | None = texture
        self.sprites: list[Sprite] = []
        self.sprite_map: Dict[str, Sprite] = {}

    def __getitem__(self, index: int) -> Sprite:
        return self.sprites[index]
    
    def add(self, sprite: Sprite):
        self.sprites.append(sprite)
        self.sprite_map[sprite.name] = sprite

    def get(self, name: str) -> Sprite:
        return self.sprite_map[name]
