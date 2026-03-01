from typing import TYPE_CHECKING

from loguru import logger

import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D

from .geom import Geom


class BoxGeom(Geom):
    def __init__(self):
        super().__init__()

    def create_shapes(
        self,
        node: "PhysicsEntity2D",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ):
        logger.debug(f"body: {node.body} width: {node.width}, height: {node.height}")
        shapes = []
        size = node.size
        half_size = size * 0.5
        shape_box = box2d.make_box(half_size.x, half_size.y)
        shape_def = box2d.ShapeDef()

        shape = node.body.create_polygon_shape(shape_def, shape_box)

        shape.friction = 10
        shape.restitution = 0.2
        shapes.append(shape)
        return shapes
