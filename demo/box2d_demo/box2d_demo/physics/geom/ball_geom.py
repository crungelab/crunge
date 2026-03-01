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

    def get_moment(self, node: "PhysicsEntity2D"):
        # size = node.size
        # radius = size.x / 2
        radius = node.model.collision_rect.width / 2 * node.scale.x
        # radius = node.radius
        return box2d.moment_for_circle(node.mass, 0, radius)

    def create_shapes(
        self,
        node: "PhysicsEntity2D",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ):
        logger.debug(f"body: {node.body} width: {node.width}, height: {node.height}")
        shapes = []
        size = node.size
        radius = node.model.collision_rect.width / 2 * node.scale.x
        circle = box2d.Circle(center=box2d.Vec2(0, 0), radius=radius)
        shape_def = box2d.ShapeDef()

        # shape = box2d.Poly.create_box(node.body, tuple(size))
        shape = node.body.create_circle_shape(shape_def, circle)

        shape.friction = 10
        shape.restitution = 0.2
        shapes.append(shape)
        return shapes

    """
    def create_shapes(
        self, node: "PhysicsEntity2D", transform: box2d.Transform = None, clip: Rect2 = None
    ):
        shapes = []
        # size = node.size
        # radius = size.x / 2
        radius = node.model.collision_rect.width / 2 * node.scale.x
        # radius = node.radius
        shape = box2d.Circle(node.body, radius)
        # shape.elasticity = 0.95
        shape.friction = 0.9
        shapes.append(shape)
        return shapes
    """
