from typing import List

from loguru import logger

from ..math.bounds3 import Bounds3

from .primitive import Primitive
from .resource import Resource

class Mesh(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.bounds = Bounds3()
        self.primitives: List[Primitive] = []

    def add_primitive(self, primitive: Primitive):
        self.primitives.append(primitive)
        self.compute_bounds()

    def compute_bounds(self):
        for primitive in self.primitives:
            self.bounds.merge(primitive.bounds)