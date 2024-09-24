from crunge.core import klass
from crunge import wgpu
from .sampler import Sampler

@klass.singleton
class DefaultSampler(Sampler):
    def __init__(self) -> None:
        sampler = self.device.create_sampler()
        super().__init__(sampler)

