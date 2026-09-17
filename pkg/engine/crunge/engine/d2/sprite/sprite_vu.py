from typing import TYPE_CHECKING

from loguru import logger

from .base_sprite_vu import BaseSpriteVu
from .sprite import Sprite, SpriteMembership
from .sprite_program import SpriteProgram

if TYPE_CHECKING:
    from .sprite_vu_group import SpriteVuGroup


class SpriteVu(BaseSpriteVu[Sprite]):
    group: "SpriteVuGroup"

    sprite_membership: SpriteMembership

    def create_program(self):
        logger.debug("SpriteVu: create_program")
        self.program = SpriteProgram()
