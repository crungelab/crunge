from typing import TYPE_CHECKING

from loguru import logger
import glm

from ..sprite.base_sprite_vu import BaseSpriteVu
from .nine_patch import NinePatch, NinePatchMembership
from .nine_patch_program import NinePatchProgram


class NinePatchVu(BaseSpriteVu[NinePatch]):
    """Nine cells from one instanced draw.

    Size comes from the node, not the model: the nine patch is shared between
    every node that joins its group, and the drawn size belongs to the node.
    Any Node2D carries one -- pass `size=` at construction or write
    `unscaled_size` later -- so there is no node class to require here.

    This only feeds `uniform.size`, which the shader lays the nine cells out
    within. Where the quad sits is Vu2D's business, off the node's rect.
    """

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
        # Reads back through the node, and Node2D.intrinsic_size falls through
        # to vu.size when a node has neither a model nor a written size: that
        # pair recurses forever. Seated on a node with a patch model or an
        # explicit size, which is every real case, it terminates on the first
        # hop. Guard here if a bare nine-patch node ever becomes a thing.
        if self.node is not None:
            return self.node.unscaled_size
        return super().size

    def create_program(self):
        logger.debug("NinePatchVu: create_program")
        self.program = NinePatchProgram()