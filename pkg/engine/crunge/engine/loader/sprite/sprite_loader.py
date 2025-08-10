from pathlib import Path

from loguru import logger
import glm

from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...d2.sprite import Sprite
from ...builder.sprite import SpriteBuilder, DefaultSpriteBuilder, CollidableSpriteBuilder

from ..loader import Loader
#from ..texture.image_texture_loader import ImageTextureLoader
from ..texture.sprite_texture_loader import SpriteTextureLoader


class SpriteLoader(Loader):
    def __init__(
        self,
        #texture_loader: ImageTextureLoader = ImageTextureLoader(),
        texture_loader: SpriteTextureLoader = SpriteTextureLoader(),
        #sprite_builder: SpriteBuilder = DefaultSpriteBuilder(),
        sprite_builder: SpriteBuilder = CollidableSpriteBuilder(),
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
        sprite = self.sprite_builder.build(texture, Rect2i(0, 0, texture.width, texture.height), color=color)
        return sprite
