from typing import List

from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import klass
from crunge import wgpu

from ..renderer import Renderer
from ..uniforms import cast_vec3, cast_matrix4

from .program_3d import Program3D
from .node_3d import Node3D
from .uniforms_3d import (
    ModelUniform,
)
from .mesh_3d import Mesh3D
from .primitive_3d import Primitive3D


@klass.singleton
class MeshInstance3DProgram(Program3D):
    pass


class MeshInstance3D(Node3D):
    def __init__(self) -> None:
        super().__init__()
        self.program = MeshInstance3DProgram()
        self.model_bind_group: wgpu.BindGroup = None
        self._mesh: Mesh3D = None

        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Uniform Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        self.build_bindgroup()

    @property
    def mesh(self) -> Mesh3D:
        return self._mesh

    @mesh.setter
    def mesh(self, mesh: Mesh3D):
        self._mesh = mesh
        self.bounds = mesh.bounds
        self.gpu_update_model()

    def update_bounds(self):
        if self.mesh:
            self.bounds = self.mesh.bounds.to_global(self.transform)
        return super().update_bounds()

    def build_bindgroup(self):
        logger.debug("Creating bind group")

        # Model
        model_bg_entries = [
            wgpu.BindGroupEntry(
                binding=0,
                buffer=self.model_uniform_buffer,
                size=self.model_uniform_buffer_size,
            ),
        ]

        model_bg_desc = wgpu.BindGroupDescriptor(
            label="Model Bind Group",
            layout=self.program.model_bind_group_layout,
            entries=model_bg_entries,
        )

        self.model_bind_group = self.device.create_bind_group(model_bg_desc)

    def gpu_update_model(self):
        model_matrix = self.transform
        normal_matrix = glm.mat4(glm.transpose(glm.inverse(glm.mat3(model_matrix))))

        model_uniform = ModelUniform()
        model_uniform.model_matrix.data = cast_matrix4(model_matrix)
        model_uniform.normal_matrix.data = cast_matrix4(normal_matrix)

        self.device.queue.write_buffer(self.model_uniform_buffer, 0, model_uniform)

    def draw(self, renderer: Renderer):
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        for primitive in self.mesh.primitives:
            primitive.draw(renderer)

        super().draw(renderer)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(3, self.model_bind_group)
