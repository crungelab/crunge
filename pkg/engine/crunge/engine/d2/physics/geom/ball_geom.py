from typing import TYPE_CHECKING

from loguru import logger

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from ..physics import Physics

from .geom import Geom


class BallGeom(Geom):
    def __init__(self, radius: float = None, clip: Rect2 = None):
        super().__init__(clip)
        self.radius = radius

    def create_shapes(
        self,
        chip: "Physics",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ) -> list:
        node = chip.node
        radius = self.radius if self.radius is not None else node.collision_radius
        logger.debug(f"BallGeom {node} radius={radius}")

        shape_def = self.make_shape_def(chip)
        circle = box2d.Circle(center=box2d.Vec2(0, 0), radius=radius)
        shape = chip.body.create_circle_shape(shape_def, circle)
        shape.user_data = chip.node

        return [shape]