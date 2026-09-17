from typing import TYPE_CHECKING
from enum import IntFlag

import glm

from ...math import Rect2i
from ...resource import SpriteTexture, Sampler
from ... import colors

from ...uniforms import cast_vec4
from ..uniforms_2d import NinePatchUniform

from ..sprite.base_sprite import BaseSprite, BaseSpriteMembership, SpriteFlipFlags

if TYPE_CHECKING:
    from .nine_patch_group import NinePatchGroup


class NinePatchFill(IntFlag):
    """How the middle cells fill their length. Unset axes stretch, which is
    what a gradient or any other non-uniform band needs."""

    STRETCH = 0
    TILE_X = 1
    TILE_Y = 2
    TILE = TILE_X | TILE_Y


class NinePatchMembership(BaseSpriteMembership[NinePatchUniform]):
    pass


class NinePatch(BaseSprite[NinePatchUniform]):
    """A subtexture drawn as nine cells: fixed corners, filling edges and centre.

    The insets are normalized fractions of the rect, so one set of insets
    survives a re-export at a different resolution. `size` stays the source
    size — the drawn size belongs to the node, since one NinePatch is shared
    by every node that joins its group.
    """

    uniform_class = NinePatchUniform

    # Class-level: BaseSprite.__init__ pushes to the GPU before this
    # subclass's __init__ body runs.
    _insets: glm.vec4 = None
    _fill: NinePatchFill = NinePatchFill.TILE
    _border_zoom: float = 1.0

    def __init__(
        self,
        texture: SpriteTexture,
        insets: glm.vec4 = None,
        rect: Rect2i = None,
        fill: NinePatchFill = NinePatchFill.TILE,
        border_zoom: float = 1.0,
        sampler: Sampler = None,
        color=colors.WHITE,
        flip_flags: SpriteFlipFlags = SpriteFlipFlags.NONE,
        texture_layer: int = 0,
        ppu: float = None,
    ) -> None:
        self._insets = glm.vec4(insets) if insets is not None else glm.vec4(0)
        self._fill = fill
        self._border_zoom = border_zoom
        super().__init__(
            texture,
            rect,
            sampler,
            color,
            flip_flags,
            texture_layer,
            ppu,
        )

    @classmethod
    def from_sprite(
        cls, sprite: BaseSprite, insets: glm.vec4 = None, **kwargs
    ) -> "NinePatch":
        """Skin from an already-loaded sprite (a loader result, an atlas entry).

        Copies rather than aliases: a nine patch has its own uniform slot, and
        the source sprite has no way to tell it when its rect changes.
        """
        return cls(
            sprite.texture,
            insets,
            sprite.rect,
            sampler=sprite.sampler,
            color=sprite.color,
            flip_flags=sprite.flip_flags,
            texture_layer=sprite.texture_layer,
            ppu=sprite.ppu,
            **kwargs,
        )

    def default_group(self) -> "NinePatchGroup":
        from .global_nine_patch_group import GlobalNinePatchGroup

        return GlobalNinePatchGroup()

    # -- insets ------------------------------------------------------------

    @property
    def insets(self) -> glm.vec4:
        return self._insets

    @insets.setter
    def insets(self, value: glm.vec4) -> None:
        self._insets = glm.vec4(value)
        self.update_gpu()

    @property
    def border_texels(self) -> glm.vec4:
        """Insets as whole texels — the form find_insets.py reports and the
        form the shader rounds to."""
        rect = self.rect
        size = glm.vec4(rect.width, rect.height, rect.width, rect.height)
        return glm.round(self._insets * size)

    @border_texels.setter
    def border_texels(self, value) -> None:
        rect = self.rect
        value = glm.vec4(value)
        self.insets = glm.vec4(
            value.x / rect.width,
            value.y / rect.height,
            value.z / rect.width,
            value.w / rect.height,
        )

    @property
    def fill(self) -> NinePatchFill:
        return self._fill

    @fill.setter
    def fill(self, value: NinePatchFill) -> None:
        self._fill = value
        self.update_gpu()

    @property
    def border_zoom(self) -> float:
        """Multiplier on the natural border thickness. 1.0 draws borders and
        tiles at their source size."""
        return self._border_zoom

    @border_zoom.setter
    def border_zoom(self, value: float) -> None:
        self._border_zoom = value
        self.update_gpu()

    # -- gpu ---------------------------------------------------------------

    def fill_uniform(self, uniform: NinePatchUniform) -> None:
        super().fill_uniform(uniform)
        uniform.insets = cast_vec4(self._insets)
        # Texels -> local units, converted here rather than baked into the
        # rect, which stays in texel space
        uniform.border_scale = self._border_zoom / self.ppu
        uniform.fill_flags = self._fill