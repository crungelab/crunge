from typing import List

from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import klass, as_capsule
from crunge import wgpu

from ..renderer import Renderer

from .program_3d import Program3D
from .node_3d import Node3D
from .vu_3d import Vu3D
from .uniforms_3d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    CameraUniform,
    ModelUniform,
)
from .primitive_3d import Primitive3D

@klass.singleton
class MeshVu3DProgram(Program3D):
    pass

class MeshVu3D(Vu3D):
    def __init__(self) -> None:
        #super().__init__()
        self.program = MeshVu3DProgram()
        self.model_bind_group: wgpu.BindGroup = None
        self.primitives: List[Primitive3D] = []

        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Uniform Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        self.build_bindgroup()
        super().__init__()

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
            entry_count=len(model_bg_entries),
            entries=model_bg_entries,
        )

        self.model_bind_group = self.device.create_bind_group(model_bg_desc)

    def add_primitive(self, primitive: Primitive3D):
        self.primitives.append(primitive)

    def gpu_update_model(self):
        model_matrix = self.transform
        normal_matrix = glm.mat4(glm.transpose(glm.inverse(glm.mat3(model_matrix))))

        model_uniform = ModelUniform()
        model_uniform.model_matrix.data = cast_matrix4(model_matrix)
        model_uniform.normal_matrix.data = cast_matrix4(normal_matrix)

        self.device.queue.write_buffer(
            self.model_uniform_buffer,
            0,
            as_capsule(model_uniform),
            self.model_uniform_buffer_size,
        )

    def draw(self, renderer: Renderer):
        pass_enc = renderer.pass_enc
        self.bind(pass_enc)
        for primitive in self.primitives:
            primitive.draw(renderer)

        super().draw(renderer)

    def bind(self, pass_enc: wgpu.RenderPassEncoder):
        pass_enc.set_bind_group(3, self.model_bind_group)