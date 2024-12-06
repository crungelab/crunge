from typing import TYPE_CHECKING

from loguru import logger

if TYPE_CHECKING:
    from crunge.engine.d2.entity import PhysicsEntity2D

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull


class Geom:
    def __init__(self):
        pass

    def create_shapes(self, node: "PhysicsEntity2D"):
        pass

    def get_moment(self, node: "PhysicsEntity2D"):
        size = node.size * node.scale
        logger.debug(f"size: {size}")
        return pymunk.moment_for_box(node.mass, tuple(size))


class BoxGeom(Geom):
    def __init__(self):
        super().__init__()

    def create_shapes(self, node: "PhysicsEntity2D", transform: pymunk.Transform = None):
        logger.debug(f"body: {node.body} width: {node.width}, height: {node.height}")
        shapes = []
        size = node.size * node.scale
        # shape = pymunk.Poly.create_box(model.body, (model.width, model.height))
        shape = pymunk.Poly.create_box(node.body, tuple(size))
        shape.friction = 10
        shape.elasticity = 0.2
        shapes.append(shape)
        return shapes


class BallGeom(Geom):
    def __init__(self):
        super().__init__()

    def get_moment(self, node: "PhysicsEntity2D"):
        size = node.size * node.scale
        radius = size.x / 2
        return pymunk.moment_for_circle(node.mass, 0, radius, (0, 0))
        # return pymunk.moment_for_circle(model.mass, 0, model.radius, (0, 0))

    def create_shapes(self, node: "PhysicsEntity2D", transform: pymunk.Transform = None):
        shapes = []
        size = node.size * node.scale
        radius = size.x / 2
        # shape = pymunk.Circle(model.body, model.radius, (0, 0))
        shape = pymunk.Circle(node.body, radius, (0, 0))
        # shape.elasticity = 0.95
        shape.friction = 0.9
        shapes.append(shape)
        return shapes


class GroupGeom(Geom):
    def __init__(self):
        super().__init__()

    def create_shapes(self, node: "PhysicsEntity2D", transform: pymunk.Transform = None):
        return []

    def get_moment(self, node: "PhysicsEntity2D"):
        return pymunk.moment_for_box(node.mass, (node.width, node.height))


class PolyGeom(Geom):
    def __init__(self):
        super().__init__()

    def get_moment(self, node: "PhysicsEntity2D"):
        size = node.size * node.scale
        return pymunk.moment_for_box(node.mass, tuple(size))
        # return pymunk.moment_for_poly(model.mass, model.sprite.points.tolist())

    """
    def get_moment(self, model):
        #return pymunk.moment_for_box(model.mass, (model.width, model.height))
        size = model.size * model.scale
        return pymunk.moment_for_box(model.mass, tuple(size))
        #return pymunk.moment_for_poly(model.mass, model.sprite.points, (-32,-32))
        #return pymunk.moment_for_circle(model.mass, 0, model.radius, (0, 0))
    """


SLOP = 0.01


class DecomposedGeom(PolyGeom):
    def __init__(self):
        super().__init__()

    def create_shapes(self, node: "PhysicsEntity2D", transform: pymunk.Transform = None):
        #transform = node.geom_transform
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
            shape = pymunk.Poly(body, poly, transform)
            shape.friction = 10
            shape.elasticity = 0.2
            shape.collision_type = node.physics.kind
            shapes.append(shape)
        return shapes


class HullGeom(PolyGeom):
    def __init__(self):
        super().__init__()

    def create_shapes(
        self, node: "PhysicsEntity2D", transform: pymunk.Transform = None
    ):
        # transform = node.geom_transform
        transform = transform if transform is not None else node.geom_transform
        body = node.body
        shapes = []

        if node.model.points is None:
            logger.debug(f"model: {node.model}: no points")
            return shapes

        points = node.model.points.tolist()
        #logger.debug(f"points: {points}")
        points = to_convex_hull(points, SLOP)

        shape = pymunk.Poly(body, points, transform)

        shape.friction = 10
        shape.elasticity = 0.2
        shape.collision_type = node.physics.kind
        shapes.append(shape)
        return shapes
