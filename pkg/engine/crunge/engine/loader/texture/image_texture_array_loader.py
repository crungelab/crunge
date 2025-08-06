from typing import List

from pathlib import Path

from loguru import logger

from ...resource.resource_manager import ResourceManager
from ...resource.texture.image_texture_array import ImageTextureArray

from ...builder.texture.image_texture_array_builder import ImageTextureArrayBuilder

from .texture_2d_loader import Texture2DLoader


class ImageTextureArrayLoader(Texture2DLoader[ImageTextureArray]):
    def load(self, paths: List[Path], name: str = None) -> ImageTextureArray:
        paths = [ResourceManager().resolve_path(path) for path in paths]

        if texture := self.kit.get_by_name(name) or self.kit.get_by_path(paths[0]):
            return texture

        image = self.image_loader.load(path)
        texture = ImageTextureArrayBuilder().build(image)
        
        self.kit.add(texture)
        return texture