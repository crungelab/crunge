from typing import TYPE_CHECKING

from loguru import logger

import glm
#from crunge import box2d
#from box2d.vec2d import Vec2d
#from box2d.autogeometry import convex_decomposition, to_convex_hull

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D


class Geom:
    def __init__(self):
        pass

    def create_shapes(self, node: "PhysicsEntity2D", transform: box2d.Transform = None, clip: Rect2 = None):
        pass

    def get_moment(self, node: "PhysicsEntity2D") -> float:
        size = node.size
        logger.debug(f"size: {size}")
        return box2d.moment_for_box(node.mass, tuple(size))


"""
ground_box = box2d.make_box(50.0, 10.0)
print("Ground Box:")
print(ground_box)

ground_shape_def = box2d.ShapeDef()
print("Ground Shape Def:")
print(ground_shape_def)

ground_shape = ground_body.create_polygon_shape(ground_shape_def, ground_box)
print("Ground Shape:")
print(ground_shape)
"""

class BoxGeom(Geom):
    def __init__(self):
        super().__init__()

    def create_shapes(
        self, node: "PhysicsEntity2D", transform: box2d.Transform = None, clip: Rect2 = None
    ):
        logger.debug(f"body: {node.body} width: {node.width}, height: {node.height}")
        shapes = []
        size = node.size
        shape_box = box2d.make_box(size.x, size.y)
        shape_def = box2d.ShapeDef()

        #shape = box2d.Poly.create_box(node.body, tuple(size))
        shape = node.body.create_polygon_shape(shape_def, shape_box)

        shape.friction = 10
        shape.restitution = 0.2
        shapes.append(shape)
        return shapes


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
        self, node: "PhysicsEntity2D", transform: box2d.Transform = None, clip: Rect2 = None
    ):
        logger.debug(f"body: {node.body} width: {node.width}, height: {node.height}")
        shapes = []
        size = node.size
        radius = node.model.collision_rect.width / 2 * node.scale.x
        circle = box2d.Circle(center=box2d.Vec2(0, 0), radius=radius)
        shape_def = box2d.ShapeDef()

        #shape = box2d.Poly.create_box(node.body, tuple(size))
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

class GroupGeom(Geom):
    def __init__(self):
        super().__init__()

    def create_shapes(
        self, node: "PhysicsEntity2D", transform: box2d.Transform = None, clip: Rect2 = None
    ):
        return []

    def get_moment(self, node: "PhysicsEntity2D"):
        return box2d.moment_for_box(node.mass, (node.width, node.height))


class PolyGeom(Geom):
    def __init__(self):
        super().__init__()

    def get_moment(self, node: "PhysicsEntity2D"):
        size = node.size
        return box2d.moment_for_box(node.mass, tuple(size))
        # return box2d.moment_for_poly(node.mass, node.model.points.tolist())

    """
    def get_moment(self, model):
        #return box2d.moment_for_box(model.mass, (model.width, model.height))
        size = model.size * model.scale
        return box2d.moment_for_box(model.mass, tuple(size))
        #return box2d.moment_for_poly(model.mass, model.sprite.points, (-32,-32))
        #return box2d.moment_for_circle(model.mass, 0, model.radius, (0, 0))
    """


SLOP = 0.01


class DecomposedGeom(PolyGeom):
    def __init__(self):
        super().__init__()

    def create_shapes(
        self, node: "PhysicsEntity2D", transform: box2d.Transform = None, clip: Rect2 = None
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


class HullGeom(PolyGeom):
    def __init__(self):
        super().__init__()

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
