from pathlib import Path

from loguru import logger
import glm

from ..math import Rect2i
from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture
from ..resource.texture.sprite_atlas import SpriteAtlas
from ..d2.sprite import Sprite
from ..builder.sprite import SpriteBuilder, SpriteAtlasBuilder

from .texture.texture_loader_base import TextureLoaderBase


class SpriteAtlasLoader(TextureLoaderBase[SpriteAtlas]):
    def __init__(self) -> None:
        super().__init__()

    def load(
        self, path: Path, rectangles: list[Rect2i], name: str = None
    ) -> SpriteAtlas:
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

        '''
        details = self.load_wgpu_texture([path])

        atlas = (
            SpriteAtlas(details.texture, glm.ivec2(details.width, details.height))
            .set_name(name)
            .set_path(path)
        )
        '''

        self.kit.add(atlas)

        for rectangle in rectangles:
            sprite = Sprite(atlas, rectangle).set_name(name)
            atlas.add(sprite)

        return atlas
