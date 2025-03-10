from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import wgpu

from ...uniforms import cast_matrix4
from ...renderer import Renderer
from ...buffer import UniformBuffer

from ..node_2d import Node2D
from ..vu_2d import Vu2D
from ..uniforms_2d import (
    ModelUniform,
)

from .background_program import BackgroundProgram
from ..sprite import Sprite


class BackgroundVu(Vu2D):
    def __init__(self, sprite: Sprite = None) -> None:
        super().__init__()
        self.sprite = sprite

        self.bind_group: wgpu.BindGroup = None
        self.buffer: UniformBuffer[ModelUniform] = None
        self._buffer_index = 0

        self.program: BackgroundProgram = None

    @property
    def buffer_index(self) -> int:
        return self._buffer_index

    @buffer_index.setter
    def buffer_index(self, value: int):
        self._buffer_index = value
        self.on_transform()

    @property
    def size(self) -> glm.vec2:
        if self.sprite is None:
            size = glm.vec2(1.0)
        size = glm.vec2(self.sprite.size)
        logger.debug(f"BackgroundVu: size: {size}")
        return size

    '''
    @property
    def size(self) -> glm.vec2:
        return glm.vec2(self.sprite.size)
    '''

    @property
    def width(self) -> float:
        return self.size.x

    @property
    def height(self) -> float:
        return self.size.y

    def on_node_model_change(self, node: Node2D) -> None:
        super().on_node_model_change(node)
        #logger.debug(f"SpriteVu: on_node_model_change: {node.model}")
        self.sprite = node.model

    def _create(self):
        super()._create()
        self.create_program()
        self.create_buffer()
        self.create_bind_group()
        return self

    def create_program(self):
        self.program = BackgroundProgram()

    def create_buffer(self):
        self.buffer = UniformBuffer(ModelUniform, 1, label="Sprite Model Buffer")

    def create_bind_group(self):
        bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.buffer.get(),
                    size=self.buffer.size,
                ),
            ]
        )

        bind_group_desc = wgpu.BindGroupDescriptor(
            label="Model Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(2),
            entry_count=len(bindgroup_entries),
            entries=bindgroup_entries,
        )

        self.bind_group = self.device.create_bind_group(bind_group_desc)

    def on_transform(self):
        super().on_transform()
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        self.buffer[self.buffer_index] = model_uniform

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.program.pipeline)
        self.sprite.bind(pass_enc)
        pass_enc.set_bind_group(2, self.bind_group)

    def draw(self, renderer: Renderer):
        # logger.debug("Drawing sprite")
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        pass_enc.draw(4)
