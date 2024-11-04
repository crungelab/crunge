from ctypes import sizeof

import glm

from crunge.core import as_capsule
from crunge import wgpu

from ..uniforms import cast_vec4
from .uniforms_2d import (
    MaterialUniform,
)

from ..resource.material import Material
from ..resource.texture import Texture

from .sprite.sprite_sampler import SpriteSampler
from .sprite.sprite_program import SpriteProgram


class Material2D(Material):
    def __init__(self, texture: Texture, color=glm.vec4(1.0, 1.0, 1.0, 1.0)) -> None:
        self._texture = texture
        self._color = color

        self.program = SpriteProgram()
        self.bind_group: wgpu.BindGroup = None
        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0

        self.create_buffers()
        self.create_bind_group()
        self.update_gpu()

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value: Texture):
        old_texture = self._texture
        self._texture = value
        if old_texture is not None and old_texture.texture != value.texture:
            self.create_bind_group()
        # logger.debug(f"Setting texture: {value}")
        self.update_gpu()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.update_gpu()

    def create_buffers(self):
        # Uniform Buffers
        self.uniform_buffer_size = sizeof(MaterialUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Material Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_group(self):
        sampler = SpriteSampler().sampler

        bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=0, sampler=sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=self.texture.view),
                wgpu.BindGroupEntry(
                    binding=2,
                    buffer=self.uniform_buffer,
                    size=self.uniform_buffer_size,
                ),
            ]
        )

        bind_group_desc = wgpu.BindGroupDescriptor(
            label="Material Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(1),
            entry_count=len(bindgroup_entries),
            entries=bindgroup_entries,
        )

        self.bind_group = self.device.create_bind_group(
            bind_group_desc
        )

    def update_gpu(self):
        uniform = MaterialUniform()
        uniform.color = cast_vec4(self.color)

        # Need to reorder because we are using a triangle strip
        uniform.uvs[0] = self.texture.coords[1]  # Top-left
        uniform.uvs[1] = self.texture.coords[2]  # Bottom-left
        uniform.uvs[2] = self.texture.coords[0]  # Top-right
        uniform.uvs[3] = self.texture.coords[3]  # Bottom-right

        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            as_capsule(uniform),
            self.uniform_buffer_size,
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(1, self.bind_group)
