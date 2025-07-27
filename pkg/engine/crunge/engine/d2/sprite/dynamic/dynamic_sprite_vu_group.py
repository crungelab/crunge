from loguru import logger

from crunge import wgpu

from ....buffer import UniformBuffer
from ...uniforms_2d import ModelUniform, NodeUniform
from ...binding_2d import DynamicModelBindGroupLayout, ModelBindGroup, DynamicNodeBindGroupLayout, NodeBindGroup

from ..sprite import Sprite
from ..sprite_vu import SpriteVu
from ..sprite_vu_group import SpriteVuGroup
from ..sprite_group import SpriteGroup

ELEMENTS = 32


class DynamicSpriteVuGroup(SpriteVuGroup):
    def __init__(self, count: int = ELEMENTS, sprite_group: SpriteGroup = None) -> None:
        super().__init__(sprite_group)
        self.is_dynamic_group = True
        self.count = count

        '''
        self.model_bind_group: DynamicModelBindGroupLayout = None
        self.model_buffer = UniformBuffer(
            ModelUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label="DynamicSpriteVuGroup Model Buffer",
        )
        logger.debug(f"Model Uniform Buffer: {self.model_buffer}")
        '''

        self.node_bind_group: DynamicNodeBindGroupLayout = None
        self.node_buffer = UniformBuffer(
            NodeUniform,
            count,
            wgpu.BufferUsage.STORAGE,
            label="DynamicSpriteVuGroup Node Buffer",
        )
        logger.debug(f"Node Uniform Buffer: {self.node_buffer}")


    def _create(self):
        super()._create()
        self.create_bind_groups()

    def append(self, vu: SpriteVu) -> None:
        super().append(vu)
        vu.group = self
        vu.node_buffer = self.node_buffer
        vu.node_buffer_index = len(self.visuals) - 1

    def remove(self, vu: SpriteVu):
        super().remove(vu)
        #vu.group = None
        for index, vu in enumerate(self.visuals):
            vu.node_buffer_index = index

    def create_bind_groups(self):
        '''
        self.model_bind_group = ModelBindGroup(
            self.model_buffer.get(),
            self.model_buffer.size,
            layout=self.program.render_pipeline.model_bind_group_layout,
        )
        '''
        self.node_bind_group = NodeBindGroup(
            self.node_buffer.get(),
            self.node_buffer.size,
            layout=self.program.render_pipeline.node_bind_group_layout,
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        #pass_enc.set_pipeline(self.program.render_pipeline.get())
        #self.model_bind_group.bind(pass_enc)
        self.sprite_group.bind(pass_enc)
        self.node_bind_group.bind(pass_enc)
