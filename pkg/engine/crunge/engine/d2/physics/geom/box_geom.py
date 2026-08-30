from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from ..physics import Physics

from .geom import Geom


class BoxGeom(Geom):
    def __init__(self, size: glm.vec2 = None, clip: Rect2 = None):
        super().__init__(clip)
        self.size = size

    def create_shapes(
        self,
        chip: "Physics",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ) -> list:
        node = chip.node
        rect = self.resolve_clip(chip, clip)

        if self.size is not None:
            half = self.size * 0.5
            center = glm.vec2(0, 0)
        elif rect is not None:
            half = glm.vec2(rect.width, rect.height) * 0.5
            center = glm.vec2(rect.x + half.x, rect.y + half.y)
        else:
            half = node.size * 0.5
            center = glm.vec2(0, 0)

        logger.debug(f"BoxGeom {node} half={half} center={center}")

        shape_def = self.make_shape_def(chip)
        if center == glm.vec2(0, 0):
            polygon = box2d.make_box(half.x, half.y)
        else:
            # ASSUMPTION: bindings emit b2MakeOffsetBox
            polygon = box2d.make_offset_box(
                half.x, half.y, box2d.Vec2(center.x, center.y), box2d.make_rot(0)
            )
        shape = chip.body.create_polygon_shape(shape_def, polygon)
        shape.user_data = chip.node

        return [shape]