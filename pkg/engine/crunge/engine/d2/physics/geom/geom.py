from typing import TYPE_CHECKING

from loguru import logger

import glm

# from crunge import box2d
# from box2d.vec2d import Vec2d
# from box2d.autogeometry import convex_decomposition, to_convex_hull

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D


class Geom:
    def __init__(self):
        pass

    def create_shapes(
        self,
        node: "PhysicsEntity2D",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ):
        pass
