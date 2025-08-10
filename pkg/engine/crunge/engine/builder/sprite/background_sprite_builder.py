from loguru import logger
import glm

from ... import colors
from ...math import Rect2i
from ...resource.sampler import Sampler
from ...resource.texture import ImageTexture
from ...d2.sprite import Sprite
from ...d2.sprite.sprite_sampler import RepeatingSpriteSampler

from .sprite_builder import SpriteBuilder

class BackgroundSpriteBuilder(SpriteBuilder):
    def build(self, texture: ImageTexture, rect: Rect2i = None, color=colors.WHITE) -> Sprite:
        logger.debug(f"Building Background Sprite: {texture.name}")
        return Sprite(texture, rect, RepeatingSpriteSampler(), color)