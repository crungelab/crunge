from pathlib import Path

from loguru import logger
import glm

from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...resource.sprite.sprite_strip import SpriteStrip
from ...d2.sprite import Sprite

from ..texture.sprite_texture_loader import SpriteTextureLoader
from .sprite_set_loader import SpriteSetLoader


class SpriteStripLoader(SpriteSetLoader[SpriteStrip]):
    def __init__(self) -> None:
        super().__init__()

    def load(self, path: Path, frame_size: glm.ivec2, frames: int, name: str = None) -> SpriteStrip:
        path = ResourceManager().resolve_path(path)
        if not name:
            name = str(path)
        if atlas := self.kit.get_by_path(path):
            return atlas

        logger.debug(f"Loading SpriteStrip: {name}")

        if not path.exists():
            raise Exception(f"Image file not found: {path}")

        texture = SpriteTextureLoader().load(path)

        atlas = SpriteStrip(texture).set_name(name).set_path(path)
        self.kit.add(atlas)

        # Iterate over each SubTexture element
        #for i in range(0, width, frame_size.x):
        for i in range(frames):
            #x = i
            x = i * frame_size.x
            y = 0
            w = frame_size.x
            h = frame_size.y

            rect = Rect2i(int(x), int(y), int(w), int(h))
            #logger.debug(f"Frame {i}: {rect}")
            # Create a new texture
            sprite = Sprite(
                texture, rect

            ).set_name(name)
            atlas.add(sprite)

        return atlas
    '''
    def load(self, path: Path, frame_size: glm.ivec2, frames: int, name: str = None) -> SpriteStrip:
        path = ResourceManager().resolve_path(path)
        if not name:
            name = str(path)
        if atlas := self.kit.get_by_path(path):
            return atlas

        logger.debug(f"Loading SpriteStrip: {name}")

        if not path.exists():
            raise Exception(f"Image file not found: {path}")

        details = self.load_wgpu_texture([path])

        atlas = SpriteStrip(details.texture, glm.ivec2(details.width, details.height)).set_name(name).set_path(path)
        self.kit.add(atlas)

        # Iterate over each SubTexture element
        #for i in range(0, width, frame_size.x):
        for i in range(frames):
            #x = i
            x = i * frame_size.x
            y = 0
            w = frame_size.x
            h = frame_size.y

            rect = Rect2i(int(x), int(y), int(w), int(h))
            #logger.debug(f"Frame {i}: {rect}")
            # Create a new texture
            sprite = Sprite(
                atlas, rect

            ).set_name(name)
            atlas.add(sprite)

        return atlas
    '''