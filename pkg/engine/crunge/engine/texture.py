import numpy as np

from crunge import wgpu
import crunge.wgpu.utils as utils


class Texture:
    name: str
    texture: wgpu.Texture
    view: wgpu.TextureView
    sampler: wgpu.Sampler

    def __init__(self, name: str) -> None:
        self.name = name