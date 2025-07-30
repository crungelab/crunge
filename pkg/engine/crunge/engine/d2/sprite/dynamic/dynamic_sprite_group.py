from loguru import logger

from crunge import wgpu

from ....buffer import UniformBuffer
from ...uniforms_2d import ModelUniform
from ...binding_2d import ModelBindGroup, DynamicModelBindGroupLayout

from ..sprite import Sprite, SpriteMembership

from ..sprite_group import SpriteGroup

ELEMENTS = 32


class DynamicSpriteGroup(SpriteGroup):
    def __init__(self, count: int = ELEMENTS) -> None:
        super().__init__()
        self.is_dynamic_group = True
        self.count = count

        self.bind_group: ModelBindGroup = None
        self.storage_buffer = UniformBuffer(
            ModelUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label="DynamicSpriteGroup Buffer",
        )
        logger.debug(f"Model Uniform Buffer: {self.storage_buffer}")

    def _create(self):
        super()._create()
        self.create_bind_group()

    def create_membership(self, sprite: Sprite) -> SpriteMembership:
        super().append(sprite)
        membership = SpriteMembership(sprite, self, self.storage_buffer, len(self.models) - 1)
        return membership

    '''
    def append(self, sprite: Sprite) -> None:
        super().append(sprite)

        membership = SpriteMembership(self, self.storage_buffer, len(self.models) - 1)
        sprite.add_membership(membership)
        return membership
    '''

    def create_bind_group(self):
        self.bind_group = ModelBindGroup(
            self.storage_buffer.get(),
            self.storage_buffer.size,
            layout=DynamicModelBindGroupLayout(),
            label="DynamicSpriteGroup Bind Group",
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.bind_group.bind(pass_enc)
