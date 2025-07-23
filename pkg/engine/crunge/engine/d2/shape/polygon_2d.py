from ctypes import sizeof

from loguru import logger
import numpy as np
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils

from ...renderer import Renderer
from ...uniforms import cast_matrix4, cast_tuple4f
from ... import colors

from ..vu_2d import Vu2D
from ..uniforms_2d import (
    ModelUniform,
    ShapeUniform,
)
from ..binding_2d import ModelBindGroup, ShapeBindGroup

from .polygon_program_2d import PolygonProgram2D

# Define the structured dtype for the combined data
vertex_dtype = np.dtype(
    [
        ("position", np.float32, (2,)),  # Points (x, y)
    ]
)


class Polygon2D(Vu2D):
    material_bind_group: ShapeBindGroup = None
    model_bind_group: ModelBindGroup = None

    vertices: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    model_uniform_buffer: wgpu.Buffer = None
    model_uniform_buffer_size: int = 0

    material_uniform_buffer: wgpu.Buffer = None
    material_uniform_buffer_size: int = 0

    def __init__(self, points: list[glm.vec2], color=colors.WHITE) -> None:
        super().__init__()
        self.points = points
        self._color = color
        self.program = PolygonProgram2D()

    def _create(self):
        super()._create()
        self.create_vertices()
        self.create_buffers()
        self.create_bind_groups()
        self.on_transform()
        self.on_material()

    @property
    def size(self) -> glm.vec2:
        return glm.vec2(1.0, 1.0)

    @property
    def width(self) -> int:
        return self.size.x

    @property
    def height(self) -> int:
        return self.size.y

    @property
    def color(self) -> glm.vec4:
        return self._color

    @color.setter
    def color(self, value: glm.vec4) -> None:
        self._color = value
        self.on_material()

    def create_vertices(self):
        # Create an empty array with the structured dtype
        self.vertices = np.empty(len(self.points) + 1, dtype=vertex_dtype)
        # Fill the array with data
        self.vertices["position"][:-1] = self.points  # Copy all points
        self.vertices["position"][-1] = self.points[
            0
        ]  # Close the loop by adding the first point again

    def update_vertices(self):
        self.create_vertices()
        utils.write_buffer(
            self.gfx.device, self.vertex_buffer, 0, self.vertices, self.vertices.nbytes
        )

    def create_buffers(self):
        self.vertex_buffer = utils.create_buffer_from_ndarray(
            self.gfx.device, "VERTEX", self.vertices, wgpu.BufferUsage.VERTEX
        )
        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

        self.material_uniform_buffer_size = sizeof(ShapeUniform)
        self.material_uniform_buffer = self.gfx.create_buffer(
            "Material Buffer",
            self.material_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        self.model_bind_group = ModelBindGroup(
            self.model_uniform_buffer,
            self.model_uniform_buffer_size,
        )
        self.material_bind_group = ShapeBindGroup(
            self.material_uniform_buffer,
            self.material_uniform_buffer_size,
        )

    def on_transform(self) -> None:
        super().on_transform()
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        self.gfx.queue.write_buffer(self.model_uniform_buffer, 0, model_uniform)

    def on_material(self) -> None:
        #super().on_material()
        material_uniform = ShapeUniform()
        material_uniform.color = cast_tuple4f(self.color)
        self.gfx.queue.write_buffer(
            self.material_uniform_buffer, 0, material_uniform
        )

    def draw(self, renderer: Renderer):
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.render_pipeline.get())
        self.model_bind_group.bind(pass_enc)
        self.material_bind_group.bind(pass_enc)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.draw(len(self.vertices), 1, 0, 0)  # Dynamic vertex count
