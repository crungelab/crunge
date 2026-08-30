from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from ..physics import Physics

from .geom import Geom


class BallGeom(Geom):
    def __init__(self, radius: float = None, offset: glm.vec2 = None, material=None):
        super().__init__(offset, material)
        self.radius = radius

    def create_shapes(self, chip: "Physics") -> list:
        node = chip.node
        radius = self.radius if self.radius is not None else node.collision_radius

        shape_def = self.make_shape_def(chip)
        circle = box2d.Circle(
            center=box2d.Vec2(self.offset.x, self.offset.y), radius=radius
        )
        shape = chip.body.create_circle_shape(shape_def, circle)
        shape.user_data = node

        return [shape]