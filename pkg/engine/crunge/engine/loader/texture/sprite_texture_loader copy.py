from pathlib import Path

from loguru import logger

from ...resource.resource_manager import ResourceManager
from ...resource.texture.sprite_texture import SpriteTexture

from ...builder.texture.sprite_texture_builder import SpriteTextureBuilder

from .texture_2d_loader import Texture2DLoader


class SpriteTextureLoader(Texture2DLoader[SpriteTexture]):
    def load(self, path: Path, name: str = None) -> SpriteTexture:
        path = ResourceManager().resolve_path(path)

        if texture := self.kit.get_by_name(name) or self.kit.get_by_path(path):
            return texture

        image = self.image_loader.load(path)
        texture = SpriteTextureBuilder().build([image])
        
        self.kit.add(texture)
        return texture