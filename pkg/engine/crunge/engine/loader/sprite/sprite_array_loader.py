from typing import Optional, List
from pathlib import Path

from loguru import logger

from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...resource.sprite.sprite_array import SpriteArray
from ...builder.sprite import SpriteBuilder, DefaultSpriteBuilder, SpriteArrayBuilder

from ..texture.texture_loader import TextureLoader


class SpriteArrayLoader(TextureLoader[SpriteArray]):
    def __init__(self, sprite_builder: SpriteBuilder = DefaultSpriteBuilder()) -> None:
        super().__init__()
        self.sprite_builder = sprite_builder

    def load(
        self, paths: List[Path], name: str = None
    ) -> SpriteArray:
        paths = [ResourceManager().resolve_path(path) for path in paths]
        # if atlas := self.kit.get_by_path(path):
        if atlas := self.kit.get_by_name(name):
            return atlas
        if atlas := self.kit.get_by_path(paths[0]):
            return atlas

        if name is None:
            name = str(paths[0])

        images = []
        
        for path in paths:
            if not path.exists():
                raise Exception(f"Image file not found: {path}")
            image = self.image_loader.load(path)
            images.append(image)

        atlas = SpriteArrayBuilder().build(images)
        atlas.set_name(name).set_path(paths[0])

        self.kit.add(atlas)

        for image in images:
            sprite = self.sprite_builder.build(atlas.texture, Rect2i(0, 0, image.size.x, image.size.y))
            atlas.add(sprite)

        return atlas
