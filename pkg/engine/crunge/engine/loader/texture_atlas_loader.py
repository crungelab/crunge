from pathlib import Path

from loguru import logger
from lxml import etree

from ..math import Rect2i
from ..resource.resource_manager import ResourceManager
from ..resource.texture import Texture
from ..resource.texture_atlas import TextureAtlas

from .texture_loader_base import TextureLoaderBase


class TextureAtlasLoader(TextureLoaderBase[TextureAtlas]):
    def __init__(self) -> None:
        super().__init__()

    def load(self, path: Path, rectangles: list[Rect2i], name: str = None) -> TextureAtlas:
        path = ResourceManager().resolve_path(path)
        #if atlas := self.kit.get_by_path(path):
        if atlas := self.kit.get_by_name(name):
            return atlas
        if atlas := self.kit.get_by_path(path):
            return atlas

        if name is None:
            name = str(path)

        details = self.load_wgpu_texture([path])

        atlas = (
            TextureAtlas(details.texture, Rect2i(0, 0, details.width, details.height))
            .set_name(name)
            .set_path(path)
        )
        self.kit.add(atlas)

        # Iterate over each SubTexture element
        for rectangle in rectangles:
            # Create a new texture
            texture = Texture(
                details.texture, rectangle, atlas
            )
            atlas.add(texture)

        return atlas
