from typing import List

from ...resource.resource_manager import ResourceManager
from ...resource.texture import ImageTexture, TextureKit
from ...resource.image import Image

from ...resource.sprite.sprite_array import SpriteArray
from ...resource.texture.image_texture import ImageTexture
from ..texture.image_texture_array_builder import ImageTextureArrayBuilder
from .sprite_set_builder import SpriteSetBuilder


class SpriteArrayBuilder(SpriteSetBuilder[SpriteArray]):
    def __init__(self, kit=ResourceManager().sprite_set_kit) -> None:
        super().__init__(texture_builder=ImageTextureArrayBuilder(), kit=kit)

    def build(self, images: List[Image]) -> SpriteArray:
        texture = self.texture_builder.build(images)
        atlas = SpriteArray(texture, images[0].size, images)
        return atlas
