from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import as_capsule
from crunge import wgpu

from ...math import Rect2i
from ...resource import ImageTexture, Material

from ...uniforms import cast_vec4
from ..uniforms_2d import (
    MaterialUniform,
)

from .sprite_sampler import SpriteSampler
from .sprite_program import SpriteProgram

'''
COORDS = [
    (0.0, 1.0),  # top-left
    (0.0, 0.0),  # bottom-left
    (1.0, 0.0),  # bottom-right
    (1.0, 1.0),  # top-right
]
'''

class Sprite(Material):
    def __init__(
        self,
        texture: ImageTexture,
        rect: Rect2i = None,
        color=glm.vec4(1.0, 1.0, 1.0, 1.0),
        points=None
    ) -> None:
        super().__init__()
        self._texture = texture
        if rect is None:
            rect = Rect2i(0, 0, texture.width, texture.height)
        self.rect = rect
        self._color = color
        self.points = points
        #self.coords = COORDS
        #self.coords = coords
        self.coords: list[tuple[float, float]] = None,
        self.update_coords()

        self.program = SpriteProgram()
        self.bind_group: wgpu.BindGroup = None
        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0

        self.create_buffers()
        self.create_bind_group()
        self.update_gpu()

    def __str__(self):
        return f"Sprite(id={self.id}, name={self.name}, path={self.path}, texture={self.texture}, rect={self.rect}, coords={self.coords})"

    def __repr__(self):
        return str(self)

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value: ImageTexture):
        old_texture = self._texture
        self._texture = value
        if old_texture is not None and old_texture.texture != value.texture:
            self.create_bind_group()
        # logger.debug(f"Setting texture: {value}")
        self.update_gpu()

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

    def update_coords(self):
        """
        Updates the texture coordinates based on the rectangle's position within the parent texture.
        """
        x = self.rect.x
        y = self.rect.y
        width = self.rect.width
        height = self.rect.height
        p_width = float(self.texture.width)
        p_height = float(self.texture.height)

        # Validate dimensions to prevent division by zero or negative coordinates
        if width <= 0 or height <= 0:
            raise ValueError("Rectangle width and height must be positive.")
        if p_width <= 0 or p_height <= 0:
            raise ValueError("Parent width and height must be positive.")

        """
        def get_texel_coords(x, y, tex_width, tex_height)
            u = (x + 0.5) / tex_width
            v = (y + 0.5) / tex_height
            return u, v
        """

        # Compute normalized texture coordinates (u, v)
        u0 = (x + 0.5) / p_width
        u1 = (x + width - 0.5) / p_width
        v0 = (y + 0.5) / p_height
        v1 = (y + height - 0.5) / p_height

        """
        u0 = x / p_width
        u1 = (x + width) / p_width
        v0 = y / p_height
        v1 = (y + height) / p_height
        """

        """
        self.coords = [
            (u0, v1),  # top-left
            (u0, v0),  # bottom-left
            (u1, v0),  # bottom-right
            (u1, v1),  # top-right
        ]
        """
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

        logger.debug(f"Texture coords updated: {self.coords}")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.update_gpu()

    def clone(self):
        return Sprite(
            self.texture,
            self.rect,
            self.color,
            self.points,
        )

    def mirror(self, horizontal: bool = False, vertical: bool = False):
        return self.clone().flip(horizontal, vertical)

    '''
    COORDS = [
        (0.0, 1.0),  # top-left
        (0.0, 0.0),  # bottom-left
        (1.0, 0.0),  # bottom-right
        (1.0, 1.0),  # top-right
    ]
    '''

    def flip(self, horizontal: bool = False, vertical: bool = False):
        """
        Flips the sprite's texture coordinates.
        """
        if horizontal:
            self.coords = [
                self.coords[3],  # top-left
                self.coords[2],  # bottom-left
                self.coords[1],  # bottom-right
                self.coords[0],  # top-right
            ]
            logger.debug(f"Flipped horizontally: {self.coords}")
        if vertical:
            self.coords = [
                self.coords[1],  # top-left
                self.coords[0],  # bottom-left
                self.coords[3],  # bottom-right
                self.coords[2],  # top-right
            ]
            logger.debug(f"Flipped vertically: {self.coords}")

        self.update_gpu()
        return self

    '''
    def flip(self, horizontal: bool = False, vertical: bool = False):
        """
        Flips the sprite's texture coordinates.
        """
        if horizontal:
            self.coords = [
                self.coords[1],  # top-left
                self.coords[0],  # bottom-left
                self.coords[3],  # bottom-right
                self.coords[2],  # top-right
            ]
            logger.debug(f"Flipped horizontally: {self.coords}")
        if vertical:
            self.coords = [
                self.coords[2],  # top-left
                self.coords[3],  # bottom-left
                self.coords[0],  # bottom-right
                self.coords[1],  # top-right
            ]
            logger.debug(f"Flipped vertically: {self.coords}")

        self.update_gpu()
        return self
    '''

    def create_buffers(self):
        # Uniform Buffers
        self.uniform_buffer_size = sizeof(MaterialUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Material Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_group(self):
        sampler = SpriteSampler().sampler

        bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=0, sampler=sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=self.texture.view),
                wgpu.BindGroupEntry(
                    binding=2,
                    buffer=self.uniform_buffer,
                    size=self.uniform_buffer_size,
                ),
            ]
        )

        bind_group_desc = wgpu.BindGroupDescriptor(
            label="Material Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(1),
            entry_count=len(bindgroup_entries),
            entries=bindgroup_entries,
        )

        self.bind_group = self.device.create_bind_group(bind_group_desc)

    def update_gpu(self):
        uniform = MaterialUniform()
        uniform.color = cast_vec4(self.color)

        # Need to reorder because we are using a triangle strip
        uniform.uvs[0] = self.coords[1]  # Top-left
        uniform.uvs[1] = self.coords[2]  # Bottom-left
        uniform.uvs[2] = self.coords[0]  # Top-right
        uniform.uvs[3] = self.coords[3]  # Bottom-right

        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            as_capsule(uniform),
            self.uniform_buffer_size,
        )

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(1, self.bind_group)
