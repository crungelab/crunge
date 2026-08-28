from ctypes import sizeof

import glm

from crunge import wgpu

from .d3.uniforms_3d import (
    AmbientLightUniform,
)

from .base import Base


class AmbientLight(Base):
    def __init__(self, color: glm.vec3 = None, energy: float = 1.0):
        # Was missing, so Base's lifetime state was never initialised.
        super().__init__()
        # None sentinel: a glm.vec3 default is one shared mutable instance
        # across every ambient light ever constructed.
        self._color = glm.vec3(1.0, 1.0, 1.0) if color is None else glm.vec3(color)
        self._energy = energy

        self.uniform_buffer: wgpu.Buffer = None
        self.uniform_buffer_size: int = 0

    def _create(self):
        super()._create()
        self.uniform_buffer_size = sizeof(AmbientLightUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Ambient Light Uniform Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        self.gpu_update_light()

    @property
    def color(self) -> glm.vec3:
        return self._color

    @color.setter
    def color(self, color: glm.vec3):
        self._color = color
        self.gpu_update_light()

    @property
    def energy(self) -> float:
        return self._energy

    @energy.setter
    def energy(self, energy: float):
        # Was a plain attribute, so changing it never reached the GPU.
        self._energy = energy
        self.gpu_update_light()

    def gpu_update_light(self):
        if self.uniform_buffer is None:
            return  # not created yet; _create writes once it is

        uniform = AmbientLightUniform()

        uniform.color.x = self.color.x
        uniform.color.y = self.color.y
        uniform.color.z = self.color.z

        uniform.energy = self.energy

        self.gfx.device.queue.write_buffer(self.uniform_buffer, 0, uniform)