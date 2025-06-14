from ctypes import sizeof

from loguru import logger
import glm

from crunge import wgpu

from ...math import Rect2i
from ...resource import ImageTexture, Material, Sampler
from ... import colors

from ...uniforms import cast_vec4, cast_vec2, cast_tuple4f
from ..uniforms_2d import (
    MaterialUniform,
)
from ..bindings_2d import BindGroupIndex, MaterialBindGroup

from .sprite_sampler import DefaultSpriteSampler
from .sprite_program import SpriteProgram

class Sprite(Material):
    def __init__(
        self,
        texture: ImageTexture,
        rect: Rect2i = None,
        sampler: Sampler = None,
        color=colors.WHITE,
        points=None,
        collision_rect: Rect2i = None,
    ) -> None:
        super().__init__()
        self._texture = texture
        if rect is None:
            rect = Rect2i(0, 0, texture.width, texture.height)
        self.flip_h = False
        self.flip_v = False

        self.sampler = sampler if sampler is not None else DefaultSpriteSampler()
        self._color = color
        self.points = points
        self.collision_rect = collision_rect
        self.program = SpriteProgram()
        #self.bind_group: wgpu.BindGroup = None
        self.bind_group: MaterialBindGroup = None
        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0

        self.create_buffers()
        self.create_bind_group()

        self._rect: Rect2i = None
        self.rect = rect

        self.update_gpu()

    def __str__(self):
        return f"Sprite(id={self.id}, name={self.name}, path={self.path}, texture={self.texture}, rect={self.rect})"

    def __repr__(self):
        return str(self)

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value: ImageTexture):
        old_texture = self._texture
        self._texture = value
        if old_texture is not None and old_texture.texture != value.texture:
            self.create_bind_group()
        # logger.debug(f"Setting texture: {value}")
        self.update_gpu()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value: Rect2i):
        self._rect = value
        self.update_gpu()

    """
    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y
    """

    @property
    def size(self):
        if self.collision_rect is not None:
            return self.collision_rect.size
        return self.rect.size

    """
    @property
    def size(self):
        return self.rect.size
    """

    @property
    def width(self):
        return self.size.x

    @property
    def height(self):
        return self.size.y

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.update_gpu()

    def clone(self):
        return Sprite(
            self.texture,
            self.rect,
            self.sampler,
            self.color,
            self.points,
        )

    def mirror(self, horizontal: bool = False, vertical: bool = False):
        return self.clone().flip(horizontal, vertical)

    def flip(self, horizontal: bool = False, vertical: bool = False):
        self.flip_h = horizontal
        self.flip_v = vertical
        self.update_gpu()
        return self

    def create_buffers(self):
        # Uniform Buffers
        self.uniform_buffer_size = sizeof(MaterialUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Material Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_group(self):
        self.bind_group = MaterialBindGroup(
            self.sampler.sampler,
            self.texture.view,
            self.uniform_buffer,
            self.uniform_buffer_size,
        )

    '''
    def create_bind_group(self):
        sampler = self.sampler.sampler

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
            entries=bindgroup_entries,
        )

        self.bind_group = self.device.create_bind_group(bind_group_desc)
    '''

    def update_gpu(self):
        uniform = MaterialUniform()
        #uniform.color = cast_vec4(self.color)
        uniform.color = cast_tuple4f(self.color)

        uniform.rect = cast_vec4(
            glm.vec4(self.rect.x, self.rect.y, self.rect.width, self.rect.height)
        )
        uniform.texture_size = cast_vec2(self.texture.size)

        uniform.flip_h = 1 if self.flip_h else 0
        uniform.flip_v = 1 if self.flip_v else 0

        self.device.queue.write_buffer(self.uniform_buffer, 0, uniform)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        #pass_enc.set_bind_group(1, self.bind_group)
        pass_enc.set_bind_group(BindGroupIndex.MATERIAL, self.bind_group.get())
