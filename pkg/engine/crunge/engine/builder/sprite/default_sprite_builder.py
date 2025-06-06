from loguru import logger
import glm

from ... import colors
from ...math import Rect2i
from ...resource.sampler import Sampler
from ...resource.texture import ImageTexture
from ...d2.sprite import Sprite

from .sprite_builder import SpriteBuilder

class DefaultSpriteBuilder(SpriteBuilder):
    def build(self, texture: ImageTexture, rect: Rect2i = None, sampler:Sampler = None, color=colors.WHITE) -> Sprite:
        #logger.debug(f"Building Sprite: {texture.image.name}")
        return Sprite(texture, rect, sampler, color)