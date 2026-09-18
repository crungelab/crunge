from crunge.core import klass

from ..uniforms_2d import ModelUniform
from ...buffer import UniformBuffer
from ..binding_2d import ModelBindGroup

from .sprite import Sprite
from .sprite_group import SpriteGroup
from .sprite import SpriteMembership


@klass.singleton
class GlobalSpriteGroup(SpriteGroup):
    def __init__(self):
        super().__init__()

    def create_membership(self, sprite: Sprite) -> SpriteMembership:
        # A buffer per membership, not a slot in a shared one. This group
        # exists for sprites whose vu draws itself, so each needs its own
        # ModelBindGroup over the single-model layout — which is why the
        # bind_group argument is filled here and left None by
        # DynamicSpriteGroup. Nothing here ever grows.

        buffer = UniformBuffer(ModelUniform, 1, label="Sprite Model Buffer")
        bind_group = ModelBindGroup(
            buffer.get(),
            buffer.size,
        )

        membership = SpriteMembership(self, sprite, 0, buffer, bind_group)
        return membership
