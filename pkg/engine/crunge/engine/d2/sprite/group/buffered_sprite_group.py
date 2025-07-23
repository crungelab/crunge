from loguru import logger

from crunge import wgpu

from ....buffer import UniformBuffer
from ...uniforms_2d import SpriteUniform
from ...binding_2d import SpriteBindGroup

from ..sprite import Sprite

from .sprite_group import SpriteGroup

ELEMENTS = 32


class BufferedSpriteGroup(SpriteGroup):
    def __init__(self, count: int = ELEMENTS) -> None:
        super().__init__()
        self.is_buffered_group = True
        self.count = count

        self.bind_group: SpriteBindGroup = None
        self.storage_buffer = UniformBuffer(
            SpriteUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label="BufferedSpriteGroup Buffer",
        )
        logger.debug(f"Sprite Uniform Buffer: {self.storage_buffer}")

    def _create(self):
        super()._create()
        self.create_bind_group()

    def append(self, sprite: Sprite) -> None:
        super().append(sprite)
        sprite.group = self
        sprite.buffer = self.storage_buffer
        sprite.buffer_index = len(self.visuals) - 1

    def create_bind_group(self):
        self.bind_group = SpriteBindGroup(
            self.storage_buffer.get(),
            self.storage_buffer.size,
            layout=self.program.render_pipeline.sprite_bind_group_layout,
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind_group.bind(pass_enc)
