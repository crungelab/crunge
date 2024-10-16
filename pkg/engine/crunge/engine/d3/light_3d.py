from ctypes import sizeof

import glm

from crunge.core import as_capsule
from crunge import wgpu

from ..math import Point3
from .node_3d import Node3D

from .uniforms_3d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    LightUniform,
)


class Light3D(Node3D):
    def __init__(self, position=Point3()) -> None:
        super().__init__(position=position)
        self._color = glm.vec3(1.0, 1.0, 1.0)
        self.energy = 1.0
        self.range = 10.0

        self.uniform_buffer_size = sizeof(LightUniform)
        self.uniform_buffer = self.gfx.create_buffer(
            "Light Uniform Buffer",
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

    def on_attached(self):
        self.scene.lighting.add_light(self)

    def on_detached(self):
        self.scene.lighting.remove_light(self)

    def gpu_update_light(self):
        light_uniform = LightUniform()

        #light_uniform.position.x = self.position.x
        #light_uniform.position.y = self.position.y
        #light_uniform.position.z = self.position.z
        light_uniform.position = cast_vec3(self.position)

        #light_uniform.color.x = self.color.x
        #light_uniform.color.y = self.color.y
        #light_uniform.color.z = self.color.z
        light_uniform.color = cast_vec3(self.color)

        light_uniform.range = self.range
        light_uniform.energy = self.energy

        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            as_capsule(light_uniform),
            self.uniform_buffer_size,
        )

class OmniLight3D(Light3D):
    pass