from typing import TYPE_CHECKING

from ctypes import Structure, c_float

from loguru import logger

from crunge import wgpu

from ..math import Rect2i

from .resource import Resource
if TYPE_CHECKING:
    from .resource_group import ResourceGroup


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


class Texture(Resource):
    def __init__(
        self,
        texture: wgpu.Texture,
        rect: Rect2i,
        parent: "Texture" = None,
    ):
        super().__init__()
        self.texture = texture
        self.rect = rect
        self.parent = parent

        self._view: wgpu.TextureView = None
        self.sampler: wgpu.Sampler = None

        self.update_coords()

    def __str__(self):
        #return f"Texture(id={self.id}, name={self.name}, path={self.path})"
        return f"Texture(id={self.id}, name={self.name}, path={self.path}, texture={self.texture}, rect={self.rect}, coords={self.coords})"

    def __repr__(self):
        return str(self)

    @property
    def view(self) -> wgpu.TextureView:
        if self._view is None:
            self._view = self.texture.create_view()
        return self._view

    @view.setter
    def view(self, view: wgpu.TextureView):
        self._view = view

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

    def add_to_group(self, group: "ResourceGroup"):
        group.texture_kit.add(self)
        return self

    def update_coords(self):
        """
        Updates the texture coordinates based on the rectangle's position within the parent texture.
        """
        if not self.parent:
            self.coords = COORDS
            return

        x = self.rect.x
        y = self.rect.y
        width = self.rect.width
        height = self.rect.height
        p_width = float(self.parent.width)
        p_height = float(self.parent.height)

        # Validate dimensions to prevent division by zero or negative coordinates
        if width <= 0 or height <= 0:
            raise ValueError("Rectangle width and height must be positive.")
        if p_width <= 0 or p_height <= 0:
            raise ValueError("Parent width and height must be positive.")

        # Compute normalized texture coordinates (u, v)
        u0 = x / p_width
        u1 = (x + width) / p_width
        v0 = y / p_height
        v1 = (y + height) / p_height

        '''
        self.coords = [
            (u0, v1),  # top-left
            (u0, v0),  # bottom-left
            (u1, v0),  # bottom-right
            (u1, v1),  # top-right
        ]
        '''
        # Flip V coordinate because texture coordinates start from bottom-left
        v0_flipped = 1.0 - v1
        v1_flipped = 1.0 - v0

        # Assign texture coordinates in the correct order
        self.coords = [
            (u0, v1_flipped),  # top-left
            (u0, v0_flipped),  # bottom-left
            (u1, v0_flipped),  # bottom-right
            (u1, v1_flipped),  # top-right
        ]

        #logger.debug(f"Texture coords updated: {self.coords}")
