from typing import TYPE_CHECKING

from loguru import logger

import glm

from crunge import box2d
from crunge.engine.math import Rect2

if TYPE_CHECKING:
    from box2d_demo.entity import PhysicsEntity2D

from .geom import Geom

class GroupGeom(Geom):
    def __init__(self):
        super().__init__()

    def create_shapes(
        self,
        node: "PhysicsEntity2D",
        transform: box2d.Transform = None,
        clip: Rect2 = None,
    ):
        return []

    def get_moment(self, node: "PhysicsEntity2D"):
        return box2d.moment_for_box(node.mass, (node.width, node.height))
