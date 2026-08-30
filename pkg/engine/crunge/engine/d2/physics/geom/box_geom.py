from typing import TYPE_CHECKING

from loguru import logger
import glm

from crunge import box2d

if TYPE_CHECKING:
    from ..physics import Physics

from .geom import Geom


class BoxGeom(Geom):
    def __init__(self, size: glm.vec2 = None, offset: glm.vec2 = None, material=None, density: float = None):
        super().__init__(offset, material, density)
        self.size = size

    def create_shapes(self, chip: "Physics") -> list:
        node = chip.node
        half = (self.size if self.size is not None else node.size) * 0.5

        logger.debug(f"BoxGeom {node} half={half} offset={self.offset}")

        shape_def = self.make_shape_def(chip)
        if self.offset == glm.vec2():
            polygon = box2d.make_box(half.x, half.y)
        else:
            # ASSUMPTION: bindings emit b2MakeOffsetBox
            polygon = box2d.make_offset_box(
                half.x, half.y,
                box2d.Vec2(self.offset.x, self.offset.y),
                box2d.make_rot(0),
            )
        shape = chip.body.create_polygon_shape(shape_def, polygon)
        shape.user_data = node

        return [shape]