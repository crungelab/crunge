from typing import TYPE_CHECKING

from loguru import logger

import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D

from .geom import Geom


class BallGeom(Geom):
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
        radius = node.collision_radius
        circle = box2d.Circle(center=box2d.Vec2(0, 0), radius=radius)
        shape_def = box2d.ShapeDef()

        shape = node.body.create_circle_shape(shape_def, circle)

        shape.user_data = node
        shape.friction = 10
        shape.restitution = 0.2
        shapes.append(shape)
        return shapes
