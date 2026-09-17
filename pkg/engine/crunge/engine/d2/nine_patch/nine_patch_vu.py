from typing import TYPE_CHECKING

from loguru import logger
import glm

from ..sprite.base_sprite_vu import BaseSpriteVu
from .nine_patch import NinePatch, NinePatchMembership
from .nine_patch_program import NinePatchProgram

if TYPE_CHECKING:
    from .nine_patch_vu_group import NinePatchVuGroup


class NinePatchVu(BaseSpriteVu[NinePatch]):
    """Nine cells from one instanced draw.

    Size comes from the node, not the model: the nine patch is shared, and
    the layout size is what the node was told to be. SizedNode2D is the node
    that carries one; without it this falls back to the source size.
    """

    group: "NinePatchVuGroup"

    sprite_membership: NinePatchMembership

    instance_count = 9

    @property
    def nine_patch(self) -> NinePatch:
        return self.sprite

    @nine_patch.setter
    def nine_patch(self, value: NinePatch) -> None:
        self.sprite = value

    @property
    def size(self) -> glm.vec2:
        if self.node is not None:
            return self.node.local_size
        return super().size

    def create_program(self):
        logger.debug("NinePatchVu: create_program")
        self.program = NinePatchProgram()
