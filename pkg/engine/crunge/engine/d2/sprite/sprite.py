from typing import TYPE_CHECKING
from ctypes import sizeof

from loguru import logger
import glm

from crunge import wgpu

from ...math import Rect2i
from ...resource import ImageTexture, Material, Sampler
from ... import colors

from ...uniforms import cast_vec4, cast_vec2, cast_tuple4f
from ..uniforms_2d import (
    SpriteUniform,
)
from ..binding_2d import SpriteBindGroup

from .sprite_sampler import DefaultSpriteSampler

if TYPE_CHECKING:
    from .sprite_group import SpriteGroup


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

        self.group: "SpriteGroup" = None

        self.bind_group: SpriteBindGroup = None

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

    def create_bind_group(self):
        self.bind_group = SpriteBindGroup(
            self.texture.view,
            self.sampler.sampler,
        )

    def update_gpu(self):
        pass        

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        self.bind_group.bind(pass_enc)
