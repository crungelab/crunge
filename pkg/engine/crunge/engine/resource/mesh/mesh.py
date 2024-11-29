from typing import List

from loguru import logger

from .primitive import Primitive
from ..resource import Resource

class Mesh(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.primitives: List[Primitive] = []

    def add_primitive(self, primitive: Primitive):
        self.primitives.append(primitive)
        self.compute_bounds()

    def compute_bounds(self):
        for primitive in self.primitives:
            self.bounds.merge(primitive.bounds)