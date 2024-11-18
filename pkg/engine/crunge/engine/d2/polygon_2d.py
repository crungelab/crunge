from ctypes import (
    Structure,
    c_float,
    c_uint32,
    sizeof,
    c_bool,
    c_int,
    c_void_p,
    cast,
    POINTER,
)

from loguru import logger
import numpy as np
import glm

# from crunge.core import klass
from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ..renderer import Renderer
from ..uniforms import cast_matrix4, cast_vec4

# from ..resource.bind_group_layout import BindGroupLayout

from .vu_2d import Vu2D
from .uniforms_2d import (
    ModelUniform,
    MaterialUniform,
)

# from .program_2d import Program2D

#from .line_program_2d import LineProgram2D
from .polygon_program_2d import PolygonProgram2D

# Define the structured dtype for the combined data
vertex_dtype = np.dtype(
    [
        ("position", np.float32, (2,)),  # Points (x, y)
    ]
)


class Polygon2D(Vu2D):
    material_bind_group: wgpu.BindGroup = None
    model_bind_group: wgpu.BindGroup = None

    vertices: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    model_uniform_buffer: wgpu.Buffer = None
    model_uniform_buffer_size: int = 0

    material_uniform_buffer: wgpu.Buffer = None
    material_uniform_buffer_size: int = 0

    def __init__(
        self, points: list[glm.vec2], color=glm.vec4(1.0, 1.0, 1.0, 1.0)
    ) -> None:
        super().__init__()
        self.points = points
        self.color = color
        #self.program = LineProgram2D()  # Assuming it is renamed to PolygonProgram2D
        self.program = PolygonProgram2D()
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

    '''
    def create_vertices(self):
        # Create an empty array with the structured dtype
        self.vertices = np.empty(len(self.points), dtype=vertex_dtype)
        # Fill the array with data
        self.vertices["position"] = self.points
    '''

    def create_vertices(self):
        # Create an empty array with the structured dtype
        self.vertices = np.empty(len(self.points) + 1, dtype=vertex_dtype)
        # Fill the array with data
        self.vertices["position"][:-1] = self.points  # Copy all points
        self.vertices["position"][-1] = self.points[0]  # Close the loop by adding the first point again

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
        model_uniform = ModelUniform()
        model_uniform.transform.data = cast_matrix4(self.transform)

        renderer.device.queue.write_buffer(
            self.model_uniform_buffer,
            0,
            as_capsule(model_uniform),
            self.model_uniform_buffer_size,
        )

        material_uniform = MaterialUniform()
        material_uniform.color = cast_vec4(self.color)

        renderer.device.queue.write_buffer(
            self.material_uniform_buffer,
            0,
            as_capsule(material_uniform),
            self.material_uniform_buffer_size,
        )

        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.pipeline)
        pass_enc.set_bind_group(1, self.material_bind_group)
        pass_enc.set_bind_group(2, self.model_bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.draw(len(self.vertices), 1, 0, 0)  # Dynamic vertex count
