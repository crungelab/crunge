from ctypes import sizeof

import glm

from crunge.core import as_capsule
from crunge import wgpu

from .renderer_3d import Renderer3D
from .node_3d import Node3D

from ..uniforms import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    CameraUniform,
    LightUniform,
)


class Light3D(Node3D):
    def __init__(self) -> None:
        super().__init__()
        self.color = glm.vec3(1.0, 1.0, 1.0)
        self.energy = 1.0
        self.range = 10.0

        self.light_uniform_buffer_size = sizeof(LightUniform)
        self.light_uniform_buffer = self.gfx.create_buffer(
            "Light Uniform Buffer",
            self.light_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def apply(self):
        light_uniform = LightUniform()

        light_uniform.position.x = self.translation.x
        light_uniform.position.y = self.translation.y
        light_uniform.position.z = self.translation.z
        # light_uniform.position = cast_vec3(self.translation)

        light_uniform.color.x = self.color.x
        light_uniform.color.y = self.color.y
        light_uniform.color.z = self.color.z
        # light_uniform.color = cast_vec3(self.color)

        light_uniform.range = self.range
        light_uniform.energy = self.energy

        self.device.queue.write_buffer(
            self.light_uniform_buffer,
            0,
            as_capsule(light_uniform),
            self.light_uniform_buffer_size,
        )

class OmniLight3D(Light3D):
    def __init__(self) -> None:
        super().__init__()
