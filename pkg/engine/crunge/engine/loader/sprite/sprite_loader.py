from pathlib import Path

from loguru import logger
import glm

from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...resource.texture import Texture
from ...resource.texture.sprite_atlas import SpriteAtlas
from ...d2.sprite import Sprite
from ...builder.sprite import SpriteBuilder, DefaultSpriteBuilder, SpriteAtlasBuilder

from ..loader import Loader
from ..texture.image_texture_loader import ImageTextureLoader


class SpriteLoader(Loader):
    def __init__(
        self,
        texture_loader: ImageTextureLoader = ImageTextureLoader(),
        sprite_builder: SpriteBuilder = DefaultSpriteBuilder(),
    ) -> None:
        super().__init__()
        self.texture_loader = texture_loader
        self.sprite_builder = sprite_builder

    def load(
        self,
        path: str | Path,
        name: str = None,
        color=glm.vec4(1.0, 1.0, 1.0, 1.0),
    ) -> Sprite:
        path = ResourceManager().resolve_path(path)
        if name is None:
            name = str(path)

        texture = self.texture_loader.load(path)
        sprite = self.sprite_builder.build(texture, color=color)
        return sprite
