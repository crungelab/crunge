from typing import TYPE_CHECKING

from loguru import logger

from crunge import wgpu

from ...math import Size2
from ...uniforms import cast_matrix4
from ...renderer import Renderer
from ...buffer import UniformBuffer

from ..vu_2d import Vu2D
from ..uniforms_2d import (
    ModelUniform,
)

from .sprite_program import SpriteProgram
from .sprite_material import SpriteMaterial

if TYPE_CHECKING:
    from .group.sprite_group import SpriteGroup


class Sprite(Vu2D):
    def __init__(self, material: SpriteMaterial) -> None:
        super().__init__()
        self.material = material

        self.bind_group: wgpu.BindGroup = None
        # self.buffer = UniformBuffer(ModelUniform, 1, label="Sprite Model Buffer")
        self.buffer: UniformBuffer[ModelUniform] = None
        # logger.debug(f"Model Uniform Buffer: {self.model_uniform_buffer}")
        self._buffer_index = 0

        # self.program = SpriteProgram()
        self.program: SpriteProgram = None
        self.group: "SpriteGroup" = None
        '''
        self.create_program()
        self.create_buffer()
        self.create_bind_group()
        '''
        self.manual_draw = True

    @property
    def buffer_index(self) -> int:
        return self._buffer_index
    
    @buffer_index.setter
    def buffer_index(self, value: int):
        self._buffer_index = value
        self.on_transform()

    @property
    def size(self) -> Size2:
        # return self.texture.size
        return Size2(self.width, self.height)

    @property
    def width(self) -> int:
        return self.material.texture.width

    @property
    def height(self) -> int:
        return self.material.texture.height

    def _create(self):
        super()._create()
        group = self.group
        if group is not None:
            group.append(self)
            if group.is_render_group:
                self.manual_draw = False

        if not self.manual_draw:
            return

        self.create_program()
        self.create_buffer()
        self.create_bind_group()
        return self

    def destroy(self):
        if self.group is not None:
            self.group.remove(self)

    '''
    def __del__(self):
        if self.group is not None:
            self.group.remove(self)
    '''

    '''
    def create(self, group: "SpriteGroup" = None, enabled=True):
        self._create(group)
        return self._post_create(enabled)

    def _create(self, group: "SpriteGroup"):
        super()._create()
        self.group = group
        if group is not None:
            group.append(self)
            if group.is_render_group:
                self.manual_draw = False

        if not self.manual_draw:
            return

        self.create_program()
        self.create_buffer()
        self.create_bind_group()
        return self
    '''

    def create_program(self):
        self.program = SpriteProgram()

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

        """
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        self.model_uniform_buffer[0] = model_uniform
        """
        #self.buffer[0].transform.data = cast_matrix4(self.transform)
        #self.buffer[self.buffer_index].transform.data = cast_matrix4(self.transform)
        #self.buffer.upload()

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_pipeline(self.program.pipeline)
        self.material.bind(pass_enc)
        pass_enc.set_bind_group(2, self.bind_group)

    def draw(self, renderer: Renderer):
        if not self.manual_draw:
            return
        # logger.debug("Drawing sprite")
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        pass_enc.draw(4)
