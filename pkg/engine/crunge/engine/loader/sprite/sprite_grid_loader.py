from pathlib import Path

from loguru import logger
import glm

from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...resource.texture.sprite_strip import SpriteStrip
from ...resource.texture.sprite_grid import SpriteGrid
from ...d2.sprite import Sprite

from ..texture.texture_loader_base import TextureLoaderBase


class SpriteGridLoader(TextureLoaderBase[SpriteStrip]):
    def __init__(self) -> None:
        super().__init__()

    def load(
        self,
        path: Path,
        frame_size: glm.ivec2,
        row_count: int,
        col_count: int,
        name: str = None,
    ) -> SpriteStrip:
        logger.debug(f"Finding SpriteGrid: {name}")
        path = ResourceManager().resolve_path(path)
        if not name:
            name = str(path)
        if atlas := self.kit.get_by_path(path):
            return atlas

        logger.debug(f"Loading SpriteGrid: {name}")

        if not path.exists():
            raise Exception(f"Image file not found: {path}")

        details = self.load_wgpu_texture([path])

        atlas = (
            SpriteGrid(details.texture, glm.ivec2(details.width, details.height))
            .set_name(name)
            .set_path(path)
        )

        self.kit.add(atlas)

        # Iterate over each SubTexture element
        for i in range(row_count):
            strip = (
                SpriteStrip(details.texture, glm.ivec2(details.width, details.height))
                .set_name(name)
                .set_path(path)
            )
            for j in range(col_count):
                x = j * frame_size.x
                y = i * frame_size.y
                w = frame_size.x
                h = frame_size.y

                rect = Rect2i(int(x), int(y), int(w), int(h))
                #logger.debug(f"Frame {i}: {rect}")
                sprite = Sprite(atlas, rect).set_name(name)
                strip.add(sprite)
            atlas.add(strip)

        return atlas
