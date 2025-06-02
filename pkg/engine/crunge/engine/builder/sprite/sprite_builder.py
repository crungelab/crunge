from loguru import logger
import glm

from ... import colors
from ...math import Rect2i
from ...resource.resource_manager import ResourceManager
from ...resource.material import MaterialKit
from ...resource.texture import ImageTexture
from ...resource.sampler import Sampler
from ...d2.sprite import Sprite

from ..resource_builder import ResourceBuilder


class SpriteBuilder(ResourceBuilder[Sprite]):
    #def __init__(self, kit: SpriteKit = ResourceManager().sprite_kit) -> None:
    def __init__(self, kit: MaterialKit = ResourceManager().material_kit) -> None:
        super().__init__(kit)

    def build(self, texture: ImageTexture, rect: Rect2i = None, sampler:Sampler = None, color=colors.WHITE) -> Sprite:
        raise NotImplementedError