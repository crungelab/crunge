from typing import TYPE_CHECKING

from loguru import logger

import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D

from .poly_geom import PolyGeom

SLOP = 0.01

class HullGeom(PolyGeom):
    def __init__(self):
        super().__init__()

    def create_shapes(
        self,
        node: "PhysicsEntity2D",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ):
        # transform = transform if transform is not None else node.geom_transform
        body = node.body
        shapes = []

        if node.model.points is None:
            # logger.debug(f"model: {node.model}: no points")
            # return shapes
            raise ValueError(f"model: {node.model}: no points")

        points = node.model.points.tolist()
        clipped_points = []
        if clip:
            for point in points:
                if clip.contains_point(glm.vec2(point[0], point[1])):
                    clipped_points.append(point)
        else:
            clipped_points = points
        # logger.debug(f"points: {points}")

        """
        b2Hull hull = b2ComputeHull( vertices, 6 );
        b2Polygon chassis = b2MakePolygon( &hull, 0.15f * scale );
        """
        hull_points = []
        for point in clipped_points:
            hull_points.append(box2d.Vec2(point[0], point[1]))

        shape_hull = box2d.compute_hull(hull_points)
        polygon = box2d.make_polygon(shape_hull, SLOP)

        shape_def = box2d.ShapeDef()
        shape = node.body.create_polygon_shape(shape_def, polygon)

        # shape.friction = 10
        # shape.elasticity = 0.2
        # shape.collision_type = node.physics.kind
        shapes.append(shape)
        return shapes

    """
    def create_shapes(
        self, node: "PhysicsEntity2D", transform: box2d.Transform = None, clip: Rect2 = None
    ):
        transform = transform if transform is not None else node.geom_transform
        body = node.body
        shapes = []

        if node.model.points is None:
            # logger.debug(f"model: {node.model}: no points")
            # return shapes
            raise ValueError(f"model: {node.model}: no points")

        points = node.model.points.tolist()
        clipped_points = []
        if clip:
            for point in points:
                if clip.contains_point(glm.vec2(point[0], point[1])):
                    clipped_points.append(point)
        else:
            clipped_points = points
        # logger.debug(f"points: {points}")
        #points = to_convex_hull(points, SLOP)
        points = to_convex_hull(clipped_points, SLOP)

        shape = box2d.Poly(body, points, transform)

        shape.friction = 10
        shape.elasticity = 0.2
        shape.collision_type = node.physics.kind
        shapes.append(shape)
        return shapes
    """
