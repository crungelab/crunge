from ctypes import Structure, c_float

from pathlib import Path

from loguru import logger
import glm

from crunge.core import utils
from crunge import wgpu

from .base import Base


class TextureCoord(Structure):
    _fields_ = [
        ("u", c_float),
        ("v", c_float),
    ]


COORDS = [
    (0.0, 1.0),  # top-left
    (0.0, 0.0),  # bottom-left
    (1.0, 0.0),  # bottom-right
    (1.0, 1.0),  # top-right
]


class Texture(Base):
    def __init__(self, texture, x, y, width, height, parent: "Texture" = None):
        self.x = x
        self.y = y
        self.texture = texture
        self.width = width
        self.height = height
        self.size = glm.vec2(width, height)
        self.parent = parent

        if parent is not None:
            p_width = float(parent.width)
            p_height = float(parent.height)
            # I'm flipping the y in the shader so I need to flip the y here
            y = p_height - y - height
            self.coords = [
                (x / p_width, (y + height) / p_height), # top-left
                (x / p_width, y / p_height), # bottom-left
                ((x + width) / p_width, y / p_height), # bottom-right
                ((x + width) / p_width, (y + height) / p_height), # top-right
            ]
        else:
            self.coords = COORDS

    def __repr__(self):
        return f"{self.__class__.__name__}({self.texture}, {self.x}, {self.y}, {self.width}, {self.height}, {self.coords})"
