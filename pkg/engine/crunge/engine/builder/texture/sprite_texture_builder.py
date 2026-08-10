from typing import TYPE_CHECKING, Dict, List
from typing import List
from pathlib import Path

from loguru import logger

from ...resource.resource_manager import ResourceManager
from ...resource.texture import SpriteTexture, TextureKit
from ...resource.image import Image

from .texture_builder import TextureBuilder


class SpriteTextureBuilder(TextureBuilder[SpriteTexture]):
    def __init__(self, kit: TextureKit = ResourceManager().texture_kit) -> None:
        super().__init__(kit)

    def build(self, images: List[Image]) -> SpriteTexture:
        wgpu_texture, im_width, im_height = self.build_wgpu_texture(images)
        return (
            SpriteTexture(wgpu_texture, images[0].size, images)
            .set_name(images[0].name)
            .set_path(images[0].path)
        )
