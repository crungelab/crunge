from loguru import logger
import glm

from crunge import wgpu

from .. import RectI
from .resource import Resource


class Sampler(Resource):
    def __init__(self, sampler: wgpu.Sampler) -> None:
        super().__init__()
        self.sampler = sampler
