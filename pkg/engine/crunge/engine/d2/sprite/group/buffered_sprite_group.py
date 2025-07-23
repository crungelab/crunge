from loguru import logger

from crunge import wgpu

from ....buffer import UniformBuffer
from ...uniforms_2d import ModelUniform
from ...binding_2d import ModelBindGroup

from ..sprite import Sprite
from ..sprite_vu import SpriteVu

from .sprite_group import SpriteGroup

ELEMENTS = 32


class BufferedSpriteGroup(SpriteGroup):
    def __init__(self, count: int = ELEMENTS) -> None:
        super().__init__()
        self.is_buffered_group = True
        self.count = count

        self.model_bind_group: ModelBindGroup = None
        self.model_storage_buffer = UniformBuffer(
            ModelUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label="BufferedSpriteGroup Buffer",
        )
        logger.debug(f"Model Uniform Buffer: {self.model_storage_buffer}")

    def _create(self):
        super()._create()
        self.create_model_bind_group()

    def append(self, vu: SpriteVu) -> None:
        super().append(vu)
        vu.group = self
        vu.buffer = self.model_storage_buffer
        vu.buffer_index = len(self.visuals) - 1

    def create_model_bind_group(self):
        self.model_bind_group = ModelBindGroup(
            self.model_storage_buffer.get(),
            self.model_storage_buffer.size,
            layout=self.program.render_pipeline.model_bind_group_layout,
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.model_bind_group.bind(pass_enc)
