from ctypes import Structure, c_float

from loguru import logger
import glm

from crunge import wgpu

from .. import Base, RectI


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
    def __init__(
        self,
        name: str,
        rect: RectI,
        texture: wgpu.Texture = None,
        parent: "Texture" = None,
    ):
        self.name = name
        self.texture = texture
        self.view: wgpu.TextureView = None
        self.sampler: wgpu.Sampler = None

        self.rect = rect
        self.parent = parent
        self.update_coords()

    def update_coords(self):
        if self.parent is not None:
            x = self.rect.x
            y = self.rect.y
            width = self.rect.width
            height = self.rect.height
            p_width = float(self.parent.width)
            p_height = float(self.parent.height)
            # I'm flipping the y in the shader so I need to flip the y here
            y = p_height - y - height
            self.coords = [
                (x / p_width, (y + height) / p_height),  # top-left
                (x / p_width, y / p_height),  # bottom-left
                ((x + width) / p_width, y / p_height),  # bottom-right
                ((x + width) / p_width, (y + height) / p_height),  # top-right
            ]
        else:
            self.coords = COORDS

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @property
    def size(self):
        return self.rect.size

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height

    def __repr__(self):
        return f"{self.__class__.__name__}({self.texture}, {self.x}, {self.y}, {self.width}, {self.height}, {self.coords})"