from ctypes import sizeof

from loguru import logger
import numpy as np
import glm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ...math import Size2
from ...resource.texture import Texture

from ..renderer_2d import Renderer2D
from ..vu_2d import Vu2D
from ..uniforms_2d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    cast_vec4,
    ModelUniform,
    MaterialUniform,
)

from .sprite_program import SpriteProgram
from .sprite_sampler import SpriteSampler


INDICES = np.array([0, 1, 2, 2, 3, 0], dtype=np.uint16)

POINTS = [
    (-0.5, 0.5),  # top-left
    (-0.5, -0.5),  # bottom-left
    (0.5, -0.5),  # bottom-right
    (0.5, 0.5),  # top-right
]

# Define the structured dtype for the combined data
vertex_dtype = np.dtype(
    [
        ("position", np.float32, (2,)),  # Points (x, y)
        ("texcoord", np.float32, (2,)),  # Texture coordinates (u, v)
    ]
)


class Sprite(Vu2D):
    material_bind_group: wgpu.BindGroup = None
    model_bind_group: wgpu.BindGroup = None

    vertices: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    indices: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = wgpu.IndexFormat.UINT16

    model_uniform_buffer: wgpu.Buffer = None
    model_uniform_buffer_size: int = 0

    material_uniform_buffer: wgpu.Buffer = None
    material_uniform_buffer_size: int = 0

    def __init__(self, texture: Texture, color=glm.vec4(1.0, 1.0, 1.0, 1.0)) -> None:
        super().__init__()
        self._texture = texture
        self.indices = INDICES
        self.points = POINTS
        self.program = SpriteProgram()
        self.create_vertices()
        self.create_buffers()
        self.create_bind_groups()

        self.color = color

    @property
    def texture(self):
        return self._texture

    @texture.setter
    def texture(self, value: Texture):
        old_texture = self._texture
        self._texture = value
        if old_texture is not None and old_texture.texture != value.texture:
            self.create_material_bind_group()
        # logger.debug(f"Setting texture: {value}")
        self.update_vertices()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        self._color = value
        self.on_color()

    def on_color(self):
        material_uniform = MaterialUniform()
        material_uniform.color = cast_vec4(self.color)

        self.device.queue.write_buffer(
            self.material_uniform_buffer,
            0,
            as_capsule(material_uniform),
            self.material_uniform_buffer_size,
        )

    @property
    def size(self) -> Size2:
        #return self.texture.size
        return Size2(self.width, self.height)

    @property
    def width(self) -> int:
        return self.texture.width

    @property
    def height(self) -> int:
        return self.texture.height

    def create_vertices(self):
        # Create an empty array with the structured dtype
        self.vertices = np.empty(len(self.points), dtype=vertex_dtype)
        # Fill the array with data
        self.vertices["position"] = self.points
        self.vertices["texcoord"] = self.texture.coords
        # logger.debug(f"Vertices: {self.vertices}")

    def update_vertices(self):
        self.create_vertices()
        utils.write_buffer(
            self.gfx.device, self.vertex_buffer, 0, self.vertices, self.vertices.nbytes
        )

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.gfx.device, "VERTEX", self.vertices, wgpu.BufferUsage.VERTEX
        )
        self.index_buffer = utils.create_buffer_from_ndarray(
            self.gfx.device, "INDEX", self.indices, wgpu.BufferUsage.INDEX
        )
        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

        self.material_uniform_buffer_size = sizeof(MaterialUniform)
        self.material_uniform_buffer = self.gfx.create_buffer(
            "Material Buffer",
            self.material_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        self.create_material_bind_group()
        self.create_model_bind_group()

    def create_material_bind_group(self):
        sampler = SpriteSampler().sampler

        material_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(binding=0, sampler=sampler),
                wgpu.BindGroupEntry(binding=1, texture_view=self.texture.view),
                wgpu.BindGroupEntry(
                    binding=2,
                    buffer=self.material_uniform_buffer,
                    size=self.material_uniform_buffer_size,
                ),
            ]
        )

        material_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Material Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(1),
            entry_count=len(material_bindgroup_entries),
            entries=material_bindgroup_entries,
        )

        self.material_bind_group = self.device.create_bind_group(
            material_bind_group_desc
        )

    def create_model_bind_group(self):
        model_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
                    buffer=self.model_uniform_buffer,
                    size=self.model_uniform_buffer_size,
                ),
            ]
        )

        model_bind_group_desc = wgpu.BindGroupDescriptor(
            label="Model Bind Group",
            layout=self.program.pipeline.get_bind_group_layout(2),
            entry_count=len(model_bindgroup_entries),
            entries=model_bindgroup_entries,
        )

        self.model_bind_group = self.device.create_bind_group(model_bind_group_desc)

    def on_transform(self):
        super().on_transform()
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        self.device.queue.write_buffer(
            self.model_uniform_buffer,
            0,
            as_capsule(model_uniform),
            self.model_uniform_buffer_size,
        )

    def draw(self, renderer: Renderer2D):
        # logger.debug("Drawing sprite")

        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.pipeline)
        pass_enc.set_bind_group(1, self.material_bind_group)
        pass_enc.set_bind_group(2, self.model_bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        pass_enc.draw_indexed(len(self.indices))
