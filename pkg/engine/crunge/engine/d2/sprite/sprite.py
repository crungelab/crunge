from typing import TYPE_CHECKING, List

from loguru import logger
import glm

from crunge import wgpu

from ...math import Rect2i
from ...resource import ImageTexture, Model, ModelMembership, Sampler
from ... import colors

from ...uniforms import cast_vec4, cast_vec2, cast_tuple4f
from ..uniforms_2d import ModelUniform
from ...buffer import UniformBuffer

from ..binding_2d import MaterialBindGroup, ModelBindGroup
from .sprite_sampler import DefaultSpriteSampler

if TYPE_CHECKING:
    from .sprite_group import SpriteGroup


class SpriteMembership(ModelMembership):
    def __init__(
        self,
        group: "SpriteGroup",
        member: "Sprite",
        index: int,
        buffer: UniformBuffer[ModelUniform],
        bind_group: ModelBindGroup = None,
    ) -> None:
        super().__init__(group, member, index)
        self.buffer: UniformBuffer[ModelUniform] = buffer
        self.bind_group = bind_group

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        if self.bind_group is not None:
            self.bind_group.bind(pass_enc)


class Sprite(Model):
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

        self.memberships: List[SpriteMembership] = []

        self.material_bind_group: MaterialBindGroup = None

        self.create_bind_groups()

        self._rect: Rect2i = None
        self.rect = rect

    def __str__(self):
        return f"Sprite(id={self.id}, name={self.name}, path={self.path}, texture={self.texture}, rect={self.rect})"

    def __repr__(self):
        return str(self)

    def join(self, group: "SpriteGroup") -> SpriteMembership:
        from .global_sprite_group import GlobalSpriteGroup

        if group is None:
            group = GlobalSpriteGroup()
        membership = self.get_membership(group)
        if membership is None:
            membership = group.create_membership(self)
            self.add_membership(membership)
        return membership

    def add_membership(self, membership: SpriteMembership) -> None:
        self.memberships.append(membership)
        self.update_gpu()

    def get_membership(self, group: "SpriteGroup") -> SpriteMembership:
        for membership in self.memberships:
            if membership.group == group:
                return membership
        return None

    def is_member_of(self, group: "SpriteGroup") -> bool:
        return any(membership.group == group for membership in self.memberships)

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value: ImageTexture):
        old_texture = self._texture
        self._texture = value
        if old_texture is not None and old_texture.texture != value.texture:
            self.create_bind_groups()
        # logger.debug(f"Setting texture: {value}")
        self.update_gpu()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value: Rect2i):
        self._rect = value
        self.update_gpu()

    @property
    def size(self):
        if self.collision_rect is not None:
            return self.collision_rect.size
        return self.rect.size

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

    def create_bind_groups(self):
        self.material_bind_group = MaterialBindGroup(
            self.texture.view,
            self.sampler.sampler,
        )

    def update_gpu(self):
        for membership in self.memberships:
            self.update_buffer(membership.buffer, membership.index)

    def update_buffer(self, buffer: UniformBuffer[ModelUniform], index: int):
        uniform = ModelUniform()
        uniform.color = cast_tuple4f(self.color)

        rect = self.rect
        uniform.rect = cast_vec4(glm.vec4(rect.x, rect.y, rect.width, rect.height))
        uniform.texture_size = cast_vec2(self.texture.size)

        uniform.flip_h = 1 if self.flip_h else 0
        uniform.flip_v = 1 if self.flip_v else 0

        try:
            buffer[index] = uniform
        except IndexError as e:
            logger.error(
                f"IndexError: {index} out of bounds for buffer of size {buffer.size}"
            )
            raise e

    def bind(self, pass_enc: wgpu.RenderPassEncoder, membership: SpriteMembership):
        self.material_bind_group.bind(pass_enc)
        membership.bind(pass_enc)
