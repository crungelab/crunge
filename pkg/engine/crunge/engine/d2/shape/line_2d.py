from ctypes import sizeof

from loguru import logger
import numpy as np
import glm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ...renderer import Renderer
from ...uniforms import cast_matrix4, cast_vec4

from ..vu_2d import Vu2D
from ..uniforms_2d import (
    ModelUniform,
    MaterialUniform,
)

from .line_program_2d import LineProgram2D

# Define the structured dtype for the combined data
vertex_dtype = np.dtype(
    [
        ("position", np.float32, (2,)),  # Points (x, y)
    ]
)

class Line2D(Vu2D):
    material_bind_group: wgpu.BindGroup = None
    model_bind_group: wgpu.BindGroup = None

    vertices: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    model_uniform_buffer: wgpu.Buffer = None
    model_uniform_buffer_size: int = 0

    material_uniform_buffer: wgpu.Buffer = None
    material_uniform_buffer_size: int = 0

    def __init__(
        self, begin: glm.vec2, end: glm.vec2, color=glm.vec4(1.0, 1.0, 1.0, 1.0)
    ) -> None:
        super().__init__()
        self.begin = begin
        self.end = end
        self.points = [begin, end]
        self.color = color
        self.program = LineProgram2D()
        self.create_vertices()
        self.create_buffers()
        self.create_bind_groups()

    @property
    def size(self) -> glm.vec2:
        return glm.vec2(1.0, 1.0)

    @property
    def width(self) -> int:
        return self.size.x

    @property
    def height(self) -> int:
        return self.size.y

    def create_vertices(self):
        # Create an empty array with the structured dtype
        self.vertices = np.empty(len(self.points), dtype=vertex_dtype)
        # Fill the array with data
        self.vertices["position"] = self.points

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

        self.material_uniform_buffer_size = sizeof(MaterialUniform)
        self.material_uniform_buffer = self.gfx.create_buffer(
            "Material Buffer",
            self.material_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def create_bind_groups(self):
        material_bindgroup_entries = wgpu.BindGroupEntries(
            [
                wgpu.BindGroupEntry(
                    binding=0,
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

    def draw(self, renderer: Renderer):
        # logger.debug("Drawing sprite")
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        renderer.device.queue.write_buffer(
            self.model_uniform_buffer,
            0,
            model_uniform
        )

        '''
        renderer.device.queue.write_buffer(
            self.model_uniform_buffer,
            0,
            as_capsule(model_uniform),
            self.model_uniform_buffer_size,
        )
        '''

        material_uniform = MaterialUniform()
        material_uniform.color = cast_vec4(self.color)

        renderer.device.queue.write_buffer(
            self.material_uniform_buffer,
            0,
            material_uniform
        )

        '''
        renderer.device.queue.write_buffer(
            self.material_uniform_buffer,
            0,
            as_capsule(material_uniform),
            self.material_uniform_buffer_size,
        )
        '''

        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.pipeline)
        pass_enc.set_bind_group(1, self.material_bind_group)
        pass_enc.set_bind_group(2, self.model_bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.draw(2, 1, 0, 0)  # Drawing 2 vertices (a single line)
