from loguru import logger
import glm

from ...math import Rect2i
from ...resource.sampler import Sampler
from ...resource.texture import ImageTexture
from ...d2.sprite import Sprite
from ...d2.sprite.sprite_sampler import RepeatingSpriteSampler

from .sprite_builder import SpriteBuilder

class BackgroundSpriteBuilder(SpriteBuilder):
    def build(self, texture: ImageTexture, rect: Rect2i = None, color=glm.vec4(1.0, 1.0, 1.0, 1.0)) -> Sprite:
    #def build(self, texture: ImageTexture, rect: Rect2i = None, sampler:Sampler = None, color=glm.vec4(1.0, 1.0, 1.0, 1.0)) -> Sprite:
        logger.debug(f"Building Background Sprite: {texture.image.name}")
        #return Sprite(texture, rect, sampler, color)
        #rect = Rect2i(0, 0, 1920, 1080)
        return Sprite(texture, rect, RepeatingSpriteSampler(), color)