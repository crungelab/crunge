
from loguru import logger

from crunge import wgpu

from ....math import Size2
from ....buffer import UniformBuffer
from ....base import Base

from ...renderer_2d import Renderer2D
from ...uniforms_2d import (
    cast_matrix4,
    ModelUniform,
)

from ..sprite_material import SpriteMaterial
from ..sprite_group import SpriteGroup
from ..sprite import Sprite

from .sprite_render_group_program import SpriteRenderGroupProgram

ELEMENTS = 32

class SpriteRenderGroup(SpriteGroup):
    def __init__(self, size: int = ELEMENTS) -> None:
        super().__init__()
        self.is_render_group = True

        self.size = size

        self.bind_group: wgpu.BindGroup = None
        self.buffer = UniformBuffer(ModelUniform, size, label="SpriteRenderGroup Buffer")
        logger.debug(f"Model Uniform Buffer: {self.buffer}")

        self.program = SpriteRenderGroupProgram()
        self.create_bind_group()

    def append(self, sprite: Sprite) -> None:
        super().append(sprite)
        sprite.buffer = self.buffer
        sprite.buffer_index = len(self.sprites) - 1

    def create_bind_group(self):
        model_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.buffer.get(),
                    size=self.buffer.size,
                ),
            ]
        )

        model_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Model Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(2),
            entry_count=len(model_bindgroup_entries),
            entries=model_bindgroup_entries,
        )

        self.bind_group = self.device.create_bind_group(model_bind_group_desc)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.program.pipeline)
        self.material.bind(pass_enc)
        pass_enc.set_bind_group(2, self.bind_group)

    def draw(self, renderer: Renderer2D):
        # logger.debug("Drawing sprite")
        pass_enc = renderer.pass_enc
        '''
        pass_enc.set_pipeline(self.program.pipeline)
        #pass_enc.set_bind_group(1, self.material_bind_group)
        self.material.bind(pass_enc)
        pass_enc.set_bind_group(2, self.model_bind_group)
        '''
        self.bind(pass_enc)
        pass_enc.draw(4)
