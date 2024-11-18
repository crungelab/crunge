from loguru import logger

import pymunk
from pymunk.vec2d import Vec2d
from pymunk.autogeometry import convex_decomposition, to_convex_hull


class Geom():
    def __init__(self):
        pass

    def create_shapes(self, model):
        pass

    def get_moment(self, model):
        size = model.size * model.scale
        logger.debug(f"size: {size}")
        return pymunk.moment_for_box(model.mass, tuple(size))


class BoxGeom(Geom):
    def __init__(self):
        super().__init__()

    def create_shapes(self, model):
        logger.debug(f"body: {model.body} width: {model.width}, height: {model.height}")
        shapes = []
        size = model.size * model.scale
        #shape = pymunk.Poly.create_box(model.body, (model.width, model.height))
        shape = pymunk.Poly.create_box(model.body, tuple(size))
        shape.friction = 10
        shape.elasticity = 0.2
        shapes.append(shape)
        return shapes

class BallGeom(Geom):
    def __init__(self):
        super().__init__()

    def get_moment(self, model):
        size = model.size * model.scale
        radius = size.x / 2
        return pymunk.moment_for_circle(model.mass, 0, radius, (0, 0))
        #return pymunk.moment_for_circle(model.mass, 0, model.radius, (0, 0))

    def create_shapes(self, model):
        shapes = []
        size = model.size * model.scale
        radius = size.x / 2
        #shape = pymunk.Circle(model.body, model.radius, (0, 0))
        shape = pymunk.Circle(model.body, radius, (0, 0))
        #shape.elasticity = 0.95
        shape.friction = 0.9
        shapes.append(shape)
        return shapes

class GroupGeom(Geom):
    def __init__(self):
        super().__init__()

    def create_shapes(self, model):
        return []
        
    def get_moment(self, model):
        return pymunk.moment_for_box(model.mass, (model.width, model.height))

class PolyGeom(Geom):
    def __init__(self):
        super().__init__()

    def get_moment(self, model):
        size = model.size * model.scale
        return pymunk.moment_for_box(model.mass, tuple(size))
        #return pymunk.moment_for_poly(model.mass, model.sprite.points.tolist())

    '''
    def get_moment(self, model):
        #return pymunk.moment_for_box(model.mass, (model.width, model.height))
        size = model.size * model.scale
        return pymunk.moment_for_box(model.mass, tuple(size))
        #return pymunk.moment_for_poly(model.mass, model.sprite.points, (-32,-32))
        #return pymunk.moment_for_circle(model.mass, 0, model.radius, (0, 0))
    '''

SLOP = 0.01
class DecomposedGeom(PolyGeom):
    def __init__(self):
        super().__init__()

    def create_shapes(self, model):
        transform = model.geom_transform

        sprite = model.sprite
        body = model.body
        position = model.position

        shapes = []
        sprite.position = position
        center = Vec2d(position)
        points = sprite.get_hit_box()
        #print(points)
        polys = convex_decomposition(points, SLOP)
        #print(polys)
        for poly in polys:
            shape = pymunk.Poly(body, poly, transform)
            shape.friction = 10
            shape.elasticity = 0.2
            shape.collision_type = model.physics.kind
            shapes.append(shape)
        return shapes

class HullGeom(PolyGeom):
    def __init__(self):
        super().__init__()

    def create_shapes(self, model, transform=None):
        transform = model.geom_transform
        body = model.body
        shapes = []

        points = model.sprite.points.tolist()

        points = to_convex_hull(points, SLOP)

        shape = pymunk.Poly(body, points, transform)

        shape.friction = 10
        shape.elasticity = 0.2
        shape.collision_type = model.physics.kind
        shapes.append(shape)
        return shapes
