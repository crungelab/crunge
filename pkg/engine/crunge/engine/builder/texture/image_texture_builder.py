from typing import TYPE_CHECKING, Dict, List
from typing import List
from pathlib import Path

from loguru import logger

from crunge import wgpu
from crunge.wgpu import utils

from ..resource_builder import ResourceBuilder

from ...resource.resource_manager import ResourceManager
from ...resource.texture import ImageTexture, TextureKit
from ...resource.image import Image

from .texture_builder import TextureBuilder


class ImageTextureBuilder(TextureBuilder[ImageTexture]):
    def __init__(self, kit: TextureKit = ResourceManager().texture_kit) -> None:
        super().__init__(kit)

    def build(self, image: Image) -> ImageTexture:
        wgpu_texture = self.build_wgpu_texture(image)
        return (
            ImageTexture(wgpu_texture, image.size, image)
            .set_name(image.name)
            .set_path(image.path)
        )

    def build_wgpu_texture(self, image: Image) -> ImageTexture:
        texture, im_width, im_height = super().build_wgpu_texture([image])
        return texture
