from typing import TYPE_CHECKING

from loguru import logger

import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D

from .poly_geom import PolyGeom

class DecomposedGeom(PolyGeom):
    def __init__(self):
        super().__init__()

    def create_shapes(
        self,
        node: "PhysicsEntity2D",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ):
        raise NotImplementedError("DecomposedGeom.create_shapes is not implemented yet")

    """
    def create_shapes(
        self,
        node: "PhysicsEntity2D",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ):
        transform = transform if transform is not None else node.geom_transform

        sprite = node.sprite
        body = node.body
        position = node.position

        shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.get_hit_box()
        # print(points)
        polys = convex_decomposition(points, SLOP)
        # print(polys)
        for poly in polys:
            shape = box2d.Poly(body, poly, transform)
            shape.friction = 10
            shape.elasticity = 0.2
            shape.collision_type = node.physics.kind
            shapes.append(shape)
        return shapes

    """