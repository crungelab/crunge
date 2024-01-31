from pathlib import Path

import imageio as iio
from loguru import logger
import glm

from crunge import wgpu, utils

from .base import Base

class Texture(Base):
    def __init__(self, texture, sampler, width, height):
        self.texture = texture
        self.sampler = sampler
        self.width = width
        self.height = height
        self.size = glm.vec2(width, height)
