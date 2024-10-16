from ctypes import sizeof

import glm

from crunge.core import as_capsule
from crunge import wgpu

from .d3.uniforms_3d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    AmbientLightUniform,
    LightUniform,
)

from .base import Base
class AmbientLight(Base):
    def __init__(self, color=glm.vec3(1.0, 1.0, 1.0), energy=1.0):
        self._color = color
        self.energy = energy

        # Uniform Buffers
        self.uniform_buffer_size = sizeof(AmbientLightUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Ambient Light Uniform Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        self.gpu_update_light()

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, color: glm.vec3):
        self._color = color
        self.gpu_update_light()

    def gpu_update_light(self):
        uniform = AmbientLightUniform()

        uniform.color.x = self.color.x
        uniform.color.y = self.color.y
        uniform.color.z = self.color.z

        uniform.energy = self.energy

        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            as_capsule(uniform),
            self.uniform_buffer_size,
        )
