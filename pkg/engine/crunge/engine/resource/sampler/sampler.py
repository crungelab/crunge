from loguru import logger

from crunge import wgpu

from ..resource import Resource


class Sampler(Resource):
    def __init__(self, sampler: wgpu.Sampler) -> None:
        super().__init__()
        self.sampler = sampler
