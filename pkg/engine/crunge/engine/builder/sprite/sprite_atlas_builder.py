from typing import TYPE_CHECKING, Dict, List
from typing import List
from pathlib import Path

from loguru import logger

from crunge import wgpu
from crunge.wgpu import utils

from ...resource.resource_manager import ResourceManager
from ...resource.texture import ImageTexture, TextureKit
from ...resource.image import Image

from ...resource.texture.sprite_atlas import SpriteAtlas

from ..texture.image_texture_builder import ImageTextureBuilder


class SpriteAtlasBuilder(ImageTextureBuilder):
    def __init__(self, kit: TextureKit = ResourceManager().texture_kit) -> None:
        super().__init__(kit)

    def build(self, image: Image) -> ImageTexture:
        wgpu_texture = self.build_wpgu_texture(image)
        #atlas = SpriteAtlas(wgpu_texture, image.size, image).set_name(image.name).set_path(image.path)
        atlas = SpriteAtlas(wgpu_texture, image.size, image)
        #self.kit.add(atlas)
        return atlas
