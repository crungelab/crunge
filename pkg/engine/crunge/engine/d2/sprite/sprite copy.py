from ctypes import sizeof

from loguru import logger
import numpy as np
import glm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ...math import Size2
from ...resource.texture import Texture

from ..renderer_2d import Renderer2D
from ..vu_2d import Vu2D
from ..uniforms_2d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    cast_vec4,
    ModelUniform,
    MaterialUniform,
    Vec4,
)

from .sprite_program import SpriteProgram
from .sprite_sampler import SpriteSampler


class Sprite(Vu2D):
    def __init__(self, texture: Texture, color=glm.vec4(1.0, 1.0, 1.0, 1.0)) -> None:
        super().__init__()
        self._texture = texture
        self._color = color

        self.material_bind_group: wgpu.BindGroup = None
        self.model_bind_group: wgpu.BindGroup = None

        self.model_uniform_buffer: wgpu.Buffer = None
        self.model_uniform_buffer_size: int = 0

        self.material_uniform_buffer: wgpu.Buffer = None
        self.material_uniform_buffer_size: int = 0

        self.program = SpriteProgram()
        self.create_buffers()
        self.create_bind_groups()

        self.update_material()

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value: Texture):
        old_texture = self._texture
        self._texture = value
        if old_texture is not None and old_texture.texture != value.texture:
            self.create_material_bind_group()
        # logger.debug(f"Setting texture: {value}")
        self.update_material()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.update_material()

    def update_material(self):
        material_uniform = MaterialUniform()
        material_uniform.color = cast_vec4(self.color)

        # Need to reorder because we are using a triangle strip
        material_uniform.uvs[0] = self.texture.coords[1]  # Top-left
        material_uniform.uvs[1] = self.texture.coords[2]  # Bottom-left
        material_uniform.uvs[2] = self.texture.coords[0]  # Top-right
        material_uniform.uvs[3] = self.texture.coords[3]  # Bottom-right

        self.device.queue.write_buffer(
            self.material_uniform_buffer,
            0,
            as_capsule(material_uniform),
            self.material_uniform_buffer_size,
        )

    @property
    def size(self) -> Size2:
        #return self.texture.size
        return Size2(self.width, self.height)

    @property
    def width(self) -> int:
        return self.texture.width

    @property
    def height(self) -> int:
        return self.texture.height

    def create_buffers(self):
        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

        self.material_uniform_buffer_size = sizeof(MaterialUniform)
        self.material_uniform_buffer = self.gfx.create_buffer(
            "Material Buffer",
            self.material_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        self.create_material_bind_group()
        self.create_model_bind_group()

    def create_material_bind_group(self):
        sampler = SpriteSampler().sampler

        material_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=0, sampler=sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=self.texture.view),
                wgpu.BindGroupEntry(
                    binding=2,
                    buffer=self.material_uniform_buffer,
                    size=self.material_uniform_buffer_size,
                ),
            ]
        )

        material_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Material Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(1),
            entry_count=len(material_bindgroup_entries),
            entries=material_bindgroup_entries,
        )

        self.material_bind_group = self.device.create_bind_group(
            material_bind_group_desc
        )

    def create_model_bind_group(self):
        model_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.model_uniform_buffer,
                    size=self.model_uniform_buffer_size,
                ),
            ]
        )

        model_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Model Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(2),
            entry_count=len(model_bindgroup_entries),
            entries=model_bindgroup_entries,
        )

        self.model_bind_group = self.device.create_bind_group(model_bind_group_desc)

    def on_transform(self):
        super().on_transform()
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        self.device.queue.write_buffer(
            self.model_uniform_buffer,
            0,
            as_capsule(model_uniform),
            self.model_uniform_buffer_size,
        )

    def draw(self, renderer: Renderer2D):
        # logger.debug("Drawing sprite")

        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.pipeline)
        pass_enc.set_bind_group(1, self.material_bind_group)
        pass_enc.set_bind_group(2, self.model_bind_group)
        pass_enc.draw(4)
