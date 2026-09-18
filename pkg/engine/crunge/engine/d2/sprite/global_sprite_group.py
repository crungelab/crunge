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
        buffer = UniformBuffer(ModelUniform, 1, label="Sprite Model Buffer")
        bind_group = ModelBindGroup(
            buffer.get(),
            buffer.size,
        )

        membership = SpriteMembership(self, sprite, 0, buffer, bind_group)
        return membership
