from typing import TYPE_CHECKING

import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from ..physics import Physics


class Geom:
    """Builds Box2D shapes for a Physics chip's body."""

    def __init__(
        self,
        offset: glm.vec2 = None,
        material=None,
        density: float = None,
        clip: Rect2 = None,
    ):
        self.offset = glm.vec2() if offset is None else glm.vec2(offset)
        self.material = material
        self.density = density
        self.clip = clip

    def create_shapes(self, chip: "Physics") -> list:
        raise NotImplementedError

    def make_shape_def(self, chip: "Physics") -> box2d.ShapeDef:
        shape_def = box2d.ShapeDef()
        shape_def.enable_contact_events = True
        material = self.material if self.material is not None else chip.material
        if material is not None:
            material.apply(shape_def)
        if self.density is not None:
            shape_def.density = self.density
        return shape_def
