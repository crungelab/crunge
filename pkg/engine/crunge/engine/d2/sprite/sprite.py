from typing import TYPE_CHECKING, List

from loguru import logger
import glm

from ...math import Rect2i
from ...resource import SpriteTexture, Sampler
from ... import colors

from ..uniforms_2d import ModelUniform

from .base_sprite import BaseSprite, BaseSpriteMembership, SpriteFlipFlags

if TYPE_CHECKING:
    from .sprite_group import SpriteGroup


class SpriteMembership(BaseSpriteMembership[ModelUniform]):
    pass


def flip_points(points, size: glm.vec2, flip: SpriteFlipFlags):
    w, h = size.x, size.y
    ax, ay = w / h, h / w

    out = []
    for p in points:
        x, y = p
        if flip & SpriteFlipFlags.DIAGONAL:
            x, y = -y * ax, -x * ay
        if flip & SpriteFlipFlags.HORIZONTAL:
            x = -x
        if flip & SpriteFlipFlags.VERTICAL:
            y = -y
        out.append((x, y))

    # Each flag is a reflection (negative determinant), so an odd number of
    # them reverses polygon winding. H|V (180 rotation) and D|H (90 CW) are
    # even and preserve it; H, V, D alone and H|V|D do not.
    if bin(int(flip)).count("1") % 2 == 1:
        out.reverse()

    return out


class Sprite(BaseSprite[ModelUniform]):
    """A subtexture drawn as one quad, sized by its rect."""

    uniform_class = ModelUniform

    def __init__(
        self,
        texture: SpriteTexture,
        rect: Rect2i = None,
        sampler: Sampler = None,
        color=colors.WHITE,
        points=None,
        collision_rect: Rect2i = None,
        flip_flags: SpriteFlipFlags = SpriteFlipFlags.NONE,
        texture_layer: int = 0,
        ppu: float = None,
    ) -> None:
        self.points = points
        self.collision_rect = collision_rect
        super().__init__(
            texture,
            rect,
            sampler,
            color,
            flip_flags,
            texture_layer,
            ppu,
        )
        self.memberships: List[SpriteMembership] = self.memberships

    @property
    def collision_size(self) -> glm.vec2:
        rect = self.collision_rect if self.collision_rect is not None else self.rect
        return glm.vec2(rect.size) / self.ppu

    def clone(self):
        return Sprite(
            self.texture,
            self.rect,
            self.sampler,
            self.color,
            self.points,
        )

    def mirror(self, flip_flags: SpriteFlipFlags):
        return self.clone().flip(flip_flags)

    def flip(self, flip_flags: SpriteFlipFlags):
        self.flip_flags = flip_flags
        self.points = flip_points(self.points, self.size, flip_flags)
        self.update_gpu()
        return self
