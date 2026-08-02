from typing import TYPE_CHECKING, List, Tuple

import math

from loguru import logger
import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D

from .poly_geom import PolyGeom

SLOP = 0.01


MAX_POLY_VERTS = 8  # Box2D default: B2_MAX_POLYGON_VERTICES


class ChainGeom(PolyGeom):
    def __init__(self):
        super().__init__()

    def create_shapes(self, node: "PhysicsEntity2D", transform=None, clip: "Rect2" = None):
        body = node.body
        scale = node.scale
        shapes = []

        if node.model.points is None:
            raise ValueError(f"model: {node.model}: no points")

        #raw = node.model.points.tolist()
        raw = node.model.points

        sx = scale.x
        sy = scale.y

        chain_points = [box2d.Vec2(x * sx, y * sy) for (x, y) in raw]
        logger.debug(f"chain_points: {chain_points}")

        #chain_def = box2d.ChainDef(points=chain_points, count=len(chain_points))
        chain_def = box2d.ChainDef(is_loop=True)
        #chain_def.points = chain_points[0]
        chain_def.count = len(chain_points)

        #body.create_chain(chain_def)
        body.create_chain_from_points(chain_def, chain_points)
        shapes.append(chain_def)

        return shapes
