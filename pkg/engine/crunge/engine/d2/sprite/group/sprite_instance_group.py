from loguru import logger

from crunge import wgpu

from ....renderer import Renderer
from ....buffer import UniformBuffer
from ...uniforms_2d import ModelUniform
from ...bindings_2d import ModelBindGroup

from ..sprite import Sprite
from ..sprite_vu import SpriteVu

from .sprite_vu_group import SpriteVuGroup
from .sprite_instance_group_program import SpriteInstanceGroupProgram

ELEMENTS = 32


class SpriteInstanceBatch:
    def __init__(self, sprite_vu: SpriteVu, first_instance: int) -> None:
        self.sprite_vu = sprite_vu
        self.first_instance = first_instance
        self.instance_count = 1


class SpriteInstanceGroup(SpriteVuGroup):
    def __init__(self, count: int = ELEMENTS) -> None:
        super().__init__()
        self.is_render_group = True
        self.count = count
        self.batches: list[SpriteInstanceBatch] = []

        self.model_bind_group: ModelBindGroup = None
        self.model_storage_buffer = UniformBuffer(
            ModelUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label="SpriteRenderGroup Buffer",
        )
        logger.debug(f"Model Uniform Buffer: {self.model_storage_buffer}")

        self.program = SpriteInstanceGroupProgram()
        self.create_model_bind_group()

    def clear(self):
        super().clear()
        self.batches.clear()

    def append(self, sprite: SpriteVu) -> None:
        super().append(sprite)
        sprite.buffer = self.model_storage_buffer
        sprite.buffer_index = len(self.visuals) - 1
        self.batch(sprite)

    def remove(self, vu):
        super().remove(vu)
        self.batch_all()

    def batch(self, member: SpriteVu):
        # Compare by texture until I start registering materials
        if len(self.batches) == 0 or self.batches[-1].sprite_vu.sprite.texture != member.sprite.texture:
            self.batches.append(
                SpriteInstanceBatch(member, member.buffer_index)
            )
        else:
            self.batches[-1].instance_count += 1

    def batch_all(self):
        self.batches.clear()
        for member in self.visuals:
            self.batch(member)

    def create_model_bind_group(self):
        self.model_bind_group = ModelBindGroup(
            self.model_storage_buffer.get(),
            self.model_storage_buffer.size,
            layout=self.program.render_pipeline.model_bind_group_layout,
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.model_bind_group.bind(pass_enc)

    def draw(self, renderer: Renderer):
        if len(self.batches) == 0:
            return
        # logger.debug("Drawing sprites")
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        for batch in self.batches:
            batch.sprite_vu.sprite.bind(pass_enc)
            pass_enc.draw(4, batch.instance_count, 0, batch.first_instance)
