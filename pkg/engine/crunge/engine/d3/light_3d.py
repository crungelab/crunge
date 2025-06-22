from loguru import logger
from ctypes import sizeof

import glm

from crunge import wgpu

from ..uniforms import cast_vec3
from .node_3d import Node3D

from .uniforms_3d import (
    LightUniform,
)


class Light3D(Node3D):
    def __init__(self, position=glm.vec3(), color=glm.vec3(1.0, 1.0, 1.0), energy=1.0, range=10.0) -> None:
        super().__init__(position=position)
        self._color = color
        self._energy = energy
        self._range = range

        self.uniform_buffer_size = sizeof(LightUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Light Uniform Buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM | wgpu.BufferUsage.COPY_DST,
        )
        self.gpu_update_model()

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, color: glm.vec3):
        self._color = color
        self.gpu_update_model()

    @property
    def energy(self):
        return self._energy

    @energy.setter
    def energy(self, energy: float):
        self._energy = energy
        self.gpu_update_model()

    @property
    def range(self):
        return self._range

    @range.setter
    def range(self, range: float):
        self._range = range
        self.gpu_update_model()

    def on_attached(self):
        self.scene.lighting.add_light(self)

    def on_detached(self):
        self.scene.lighting.remove_light(self)

    def gpu_update_model(self):
        super().gpu_update_model()
        light_uniform = LightUniform()

        light_uniform.position = cast_vec3(self.position)
        light_uniform.color = cast_vec3(self.color)

        light_uniform.energy = self.energy
        light_uniform.range = self.range

        self.device.queue.write_buffer(self.uniform_buffer, 0, light_uniform)


class OmniLight3D(Light3D):
    pass
