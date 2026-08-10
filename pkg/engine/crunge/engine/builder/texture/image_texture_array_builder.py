from typing import TYPE_CHECKING, Dict, List
from typing import List

from loguru import logger

from ...resource.resource_manager import ResourceManager
from ...resource.texture import ImageTextureArray, TextureKit
from ...resource.image import Image

from .texture_builder import TextureBuilder


class ImageTextureArrayBuilder(TextureBuilder[ImageTextureArray]):
    def __init__(self, kit: TextureKit = ResourceManager().texture_kit) -> None:
        super().__init__(kit)

    def build(self, images: List[Image]) -> ImageTextureArray:
        wgpu_texture, im_width, im_height = self.build_wgpu_texture(images)
        return (
            ImageTextureArray(wgpu_texture, images[0].size, images[0])
            .set_name(images[0].name)
            .set_path(images[0].path)
        )
