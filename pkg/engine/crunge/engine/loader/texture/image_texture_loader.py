from pathlib import Path

from loguru import logger
import glm

from ...resource.resource_manager import ResourceManager
from ...resource.texture import Texture2D
from ...resource.texture.image_texture import ImageTexture

from ...builder.texture.image_texture_builder import ImageTextureBuilder

from .texture_2d_loader import Texture2DLoader


class ImageTextureLoader(Texture2DLoader[ImageTexture]):
    def load(self, path: Path, name: str = None) -> ImageTexture:
        path = ResourceManager().resolve_path(path)

        if texture := self.kit.get_by_name(name) or self.kit.get_by_path(path):
            return texture

        #details = self.load_wgpu_texture([path])
        #texture = ImageTexture(details.texture, glm.ivec2(details.width, details.height), details.image).set_name(name).set_path(path)
        image = self.image_loader.load(path)
        #texture = ImageTexture(image.texture, glm.ivec2(image.width, image.height), image).set_name(name).set_path(path)
        texture = ImageTextureBuilder().build(image)
        
        self.kit.add(texture)
        return texture