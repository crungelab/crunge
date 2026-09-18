from loguru import logger

from crunge import wgpu

from ....buffer import UniformBuffer
from ...uniforms_2d import ModelUniform
from ...binding_2d import DynamicModelBindGroup

from ..sprite import Sprite, SpriteMembership

from ..sprite_group import SpriteGroup

ELEMENTS = 256


class DynamicSpriteGroup(SpriteGroup):
    def __init__(self, count: int = ELEMENTS) -> None:
        super().__init__()
        self.count = count

        self.bind_group: DynamicModelBindGroup = None
        self.storage_buffer = UniformBuffer(
            ModelUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label="DynamicSpriteGroup Buffer",
        )
        self.storage_buffer.resized.connect(self.on_storage_buffer_resized)
        logger.debug(f"Model Uniform Buffer: {self.storage_buffer}")
        self.create_bind_group()

    def _create(self):
        super()._create()
        self.create_bind_group()

    def create_membership(self, sprite: Sprite) -> SpriteMembership:
        super().append(sprite)
        index = len(self.memberships) - 1
        # Before the membership exists, so the slot it is about to be given
        # is allocated. `count` follows the buffer rather than the
        # constructor argument, which is now a starting size.
        self.storage_buffer.ensure(index + 1)
        self.count = self.storage_buffer.count
        return SpriteMembership(self, sprite, index, self.storage_buffer)

    '''
    def create_membership(self, sprite: Sprite) -> SpriteMembership:
        super().append(sprite)
        membership = SpriteMembership(
            self, sprite, len(self.memberships) - 1, self.storage_buffer
        )
        return membership
    '''

    def create_bind_group(self):
        # No layout= argument. The type fixes it, so this group can no
        # longer be handed the single-model layout by omission.
        self.bind_group = DynamicModelBindGroup(
            self.storage_buffer.get(),
            self.storage_buffer.size,
            label="DynamicSpriteGroup Bind Group",
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.bind_group.bind(pass_enc)

    def on_storage_buffer_resized(self, buffer) -> None:
        # The old bind group points at a buffer that no longer holds the
        # data. Every holder of one over this buffer has to rebuild, or it
        # binds a handle the shader reads nothing from.
        self.create_bind_group()