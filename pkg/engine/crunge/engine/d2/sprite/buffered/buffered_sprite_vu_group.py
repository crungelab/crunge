from loguru import logger

from crunge import wgpu

from ....buffer import UniformBuffer
from ...uniforms_2d import ModelUniform
from ...binding_2d import ModelBindGroup

from ..sprite import Sprite
from ..sprite_vu import SpriteVu
from ..sprite_vu_group import SpriteVuGroup

ELEMENTS = 32


class BufferedSpriteVuGroup(SpriteVuGroup):
    def __init__(self, count: int = ELEMENTS) -> None:
        super().__init__()
        self.is_buffered_group = True
        self.count = count

        self.bind_group: ModelBindGroup = None
        self.storage_buffer = UniformBuffer(
            ModelUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label="BufferedSpriteVuGroup Buffer",
        )
        logger.debug(f"Model Uniform Buffer: {self.storage_buffer}")

    def _create(self):
        super()._create()
        self.create_bind_group()

    def append(self, vu: SpriteVu) -> None:
        super().append(vu)
        #vu.group = self
        vu.buffer = self.storage_buffer
        vu.buffer_index = len(self.visuals) - 1

    def create_bind_group(self):
        self.bind_group = ModelBindGroup(
            self.storage_buffer.get(),
            self.storage_buffer.size,
            layout=self.program.render_pipeline.model_bind_group_layout,
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.bind_group.bind(pass_enc)
