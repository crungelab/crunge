from loguru import logger
import glm

from crunge.engine.d2.settings_2d import Settings2D

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
    def __init__(self, kit: MaterialKit = ResourceManager().material_kit, ppu: float = None) -> None:
        super().__init__(kit)
        self.ppu = ppu if ppu is not None else Settings2D().ppu

    def build(self, texture: ImageTexture, rect: Rect2i = None, sampler:Sampler = None, color=colors.WHITE) -> Sprite:
        raise NotImplementedError