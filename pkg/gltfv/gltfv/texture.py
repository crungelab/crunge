import numpy as np

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from .node import Node

class Texture:
    texture: wgpu.Texture
    view: wgpu.TextureView
    sampler: wgpu.Sampler

    def __init__(self) -> None:
        pass