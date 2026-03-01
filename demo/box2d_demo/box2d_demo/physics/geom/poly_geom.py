from typing import TYPE_CHECKING

from loguru import logger

import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D

from .geom import Geom


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
