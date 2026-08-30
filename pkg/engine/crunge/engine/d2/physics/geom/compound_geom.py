from typing import TYPE_CHECKING, List

import glm

if TYPE_CHECKING:
    from ..physics import Physics

from .geom import Geom


class CompoundGeom(Geom):
    """Several geoms on one body. Child offsets stack on this geom's own."""

    def __init__(self, children: List[Geom], offset: glm.vec2 = None, material=None):
        super().__init__(offset, material)
        self.children = children

    def create_shapes(self, chip: "Physics") -> list:
        shapes = []
        for child in self.children:
            child_offset = child.offset
            if self.offset != glm.vec2():
                child.offset = child_offset + self.offset
            try:
                if child.material is None:
                    child.material = self.material
                shapes.extend(child.create_shapes(chip))
            finally:
                child.offset = child_offset
        return shapes