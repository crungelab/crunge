from pathlib import Path

from loguru import logger

from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...resource.texture.sprite_array import SpriteArray
from ...builder.sprite import SpriteBuilder, DefaultSpriteBuilder, SpriteAtlasBuilder

from ..texture.texture_loader_base import TextureLoaderBase


class SpriteArrayLoader(TextureLoaderBase[SpriteArray]):
    def __init__(self, sprite_builder: SpriteBuilder = DefaultSpriteBuilder()) -> None:
        super().__init__()
        self.sprite_builder = sprite_builder

    def load(
        self, path: Path, rectangles: list[Rect2i], name: str = None
    ) -> SpriteArray:
        path = ResourceManager().resolve_path(path)
        # if atlas := self.kit.get_by_path(path):
        if atlas := self.kit.get_by_name(name):
            return atlas
        if atlas := self.kit.get_by_path(path):
            return atlas

        if name is None:
            name = str(path)

        image = self.image_loader.load(path)
        atlas = SpriteAtlasBuilder().build(image)
        atlas.set_name(name).set_path(path)

        self.kit.add(atlas)

        for rectangle in rectangles:
            sprite = self.sprite_builder.build(atlas, rectangle)
            atlas.add(sprite)

        return atlas
