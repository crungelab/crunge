from typing import List

from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import as_capsule
from crunge import wgpu

from .primitive import Primitive

from .resource import Resource


class Mesh(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.primitives: List[Primitive] = []

    def add_primitive(self, primitive: Primitive):
        self.primitives.append(primitive)
