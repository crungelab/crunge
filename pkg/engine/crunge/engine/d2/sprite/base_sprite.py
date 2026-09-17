from typing import TYPE_CHECKING, ClassVar, List, Type
from enum import IntFlag

from loguru import logger
import glm

from crunge import wgpu

from ...math import Rect2i
from ...resource import SpriteTexture, Model, ModelMembership, Sampler
from ... import colors

from ...uniforms import cast_vec4, cast_vec2, cast_tuple4f
from ..uniforms_2d import ModelUniform
from ...buffer import UniformBuffer

from ..settings_2d import Settings2D
from ..binding_2d import MaterialBindGroup, ModelBindGroup
from .sprite_sampler import DefaultSpriteSampler

if TYPE_CHECKING:
    from .base_sprite_group import BaseSpriteGroup


class SpriteFlipFlags(IntFlag):
    NONE = 0
    HORIZONTAL = 1
    VERTICAL = 2
    DIAGONAL = 4  # transpose — applied before H/V


class BaseSpriteMembership[UniformT](ModelMembership):
    def __init__(
        self,
        group: "BaseSpriteGroup",
        member: "BaseSprite",
        index: int,
        buffer: UniformBuffer[UniformT],
        bind_group: ModelBindGroup = None,
    ) -> None:
        super().__init__(group, member, index)
        self.buffer: UniformBuffer[UniformT] = buffer
        self.bind_group = bind_group

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        if self.bind_group is not None:
            self.bind_group.bind(pass_enc)


class BaseSprite[UniformT](Model):
    """A texture, a subtexture rect, and the uniform slot they are drawn from.

    Subclasses decide what `size` means and what else goes in the uniform:
    a Sprite's size follows its rect, a NinePatch is sized by its node.
    """

    uniform_class: ClassVar[Type] = ModelUniform

    def __init__(
        self,
        texture: SpriteTexture,
        rect: Rect2i = None,
        sampler: Sampler = None,
        color=colors.WHITE,
        flip_flags: SpriteFlipFlags = SpriteFlipFlags.NONE,
        texture_layer: int = 0,
        ppu: float = None,
    ) -> None:
        super().__init__()
        self._texture = texture
        if rect is None:
            rect = Rect2i(0, 0, texture.width, texture.height)
        self.flip_flags = flip_flags

        self.sampler = sampler if sampler is not None else DefaultSpriteSampler()
        self.texture_layer = texture_layer
        self._color = color
        self.ppu = ppu if ppu is not None else Settings2D().ppu

        self.memberships: List[BaseSpriteMembership[UniformT]] = []

        self.material_bind_group: MaterialBindGroup = None

        self.create_bind_groups()

        # Last: the setter pushes to the GPU, so everything it reads must
        # already be set. Subclass fields have class-level defaults for the
        # same reason — this runs before their __init__ body.
        self._rect: Rect2i = None
        self.rect = rect

    def __str__(self):
        return (
            f"{type(self).__name__}(id={self.id}, name={self.name}, path={self.path}, "
            f"texture={self.texture}, rect={self.rect})"
        )

    def __repr__(self):
        return str(self)

    # -- flips -------------------------------------------------------------

    @property
    def flip_h(self) -> bool:
        return bool(self.flip_flags & SpriteFlipFlags.HORIZONTAL)

    @property
    def flip_v(self) -> bool:
        return bool(self.flip_flags & SpriteFlipFlags.VERTICAL)

    @property
    def flip_d(self) -> bool:
        return bool(self.flip_flags & SpriteFlipFlags.DIAGONAL)

    # -- group membership --------------------------------------------------

    def default_group(self) -> "BaseSpriteGroup":
        """The group joined when none is given. Overridden per uniform type:
        a group's buffer stride is its members' uniform size."""
        from .global_sprite_group import GlobalSpriteGroup

        return GlobalSpriteGroup()

    def join(self, group: "BaseSpriteGroup" = None) -> BaseSpriteMembership[UniformT]:
        if group is None:
            group = self.default_group()
        membership = self.get_membership(group)
        if membership is None:
            membership = group.create_membership(self)
            self.add_membership(membership)
        return membership

    def add_membership(self, membership: BaseSpriteMembership[UniformT]) -> None:
        self.memberships.append(membership)
        self.update_gpu()

    def get_membership(
        self, group: "BaseSpriteGroup"
    ) -> BaseSpriteMembership[UniformT]:
        for membership in self.memberships:
            if membership.group == group:
                return membership
        return None

    def is_member_of(self, group: "BaseSpriteGroup") -> bool:
        return any(membership.group == group for membership in self.memberships)

    # -- texture and rect --------------------------------------------------

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value: SpriteTexture):
        old_texture = self._texture
        self._texture = value
        if old_texture is not None and old_texture.texture != value.texture:
            self.create_bind_groups()
        self.update_gpu()

    @property
    def rect(self):
        return self._rect

    @rect.setter
    def rect(self, value: Rect2i):
        self._rect = value
        self.update_gpu()

    @property
    def size(self) -> glm.vec2:
        return glm.vec2(self.rect.size) / self.ppu

    @property
    def collision_size(self) -> glm.vec2:
        return self.size

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

    # -- gpu ---------------------------------------------------------------

    def create_bind_groups(self):
        self.material_bind_group = MaterialBindGroup(
            self.texture.view,
            self.sampler.sampler,
        )

    def update_gpu(self):
        for membership in self.memberships:
            self.update_buffer(membership.buffer, membership.index)

    def fill_uniform(self, uniform: UniformT) -> None:
        """Head-call super, then set the fields this subclass adds — the same
        shape as the WGSL structs, which share their first 48 bytes."""
        uniform.color = cast_tuple4f(self.color)

        rect = self.rect
        uniform.rect = cast_vec4(glm.vec4(rect.x, rect.y, rect.width, rect.height))
        uniform.texture_size = cast_vec2(self.texture.size)

        uniform.flip_flags = self.flip_flags

        uniform.texture_layer = self.texture_layer

    def update_buffer(self, buffer: UniformBuffer[UniformT], index: int) -> None:
        uniform = self.uniform_class()
        self.fill_uniform(uniform)

        try:
            buffer[index] = uniform
        except IndexError as e:
            logger.error(
                f"IndexError: {index} out of bounds for buffer of size {buffer.size}"
            )
            raise e

    def bind(
        self,
        pass_enc: wgpu.RenderPassEncoder,
        membership: BaseSpriteMembership[UniformT],
    ):
        self.material_bind_group.bind(pass_enc)
        membership.bind(pass_enc)
