from crunge import wgpu

from ...resource.model import ModelGroup

from .base_sprite import BaseSprite, BaseSpriteMembership


class BaseSpriteGroup[MemberT: BaseSprite, MembershipT: BaseSpriteMembership](
    ModelGroup[MembershipT]
):
    """A uniform buffer's worth of sprites. Subclasses differ by uniform
    type, which sets the buffer's stride."""

    def __init__(self):
        super().__init__()
        self.is_dynamic_group = False

    def create_membership(self, member: MemberT) -> MembershipT:
        raise NotImplementedError(
            f"{type(self).__name__}.create_membership should be implemented in subclasses"
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder) -> None:
        raise NotImplementedError(
            f"{type(self).__name__}.bind should be implemented in subclasses"
        )
