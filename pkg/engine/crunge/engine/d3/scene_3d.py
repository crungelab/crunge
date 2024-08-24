from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import as_capsule
from crunge import wgpu

from ..light import AmbientLight

from .uniforms import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    AmbientLightUniform,
    LightUniform,
)

from .node_3d import Node3D
from .scene_renderer_3d import SceneRenderer3D

class Scene3D(Node3D):
    def __init__(self) -> None:
        super().__init__()
        self.scene = self

        self.ambient_light = AmbientLight()
        
        # Uniform Buffers
        self.ambient_light_uniform_buffer_size = sizeof(AmbientLightUniform)
        self.ambient_light_uniform_buffer = self.gfx.create_buffer(
            "Ambient Light Uniform Buffer",
            self.ambient_light_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def draw(self, renderer: SceneRenderer3D):
            ambient_light = self.ambient_light

            ambient_light_uniform = AmbientLightUniform()

            #0.0, 0.502, 1.0
            ambient_light_uniform.color.x = ambient_light.color.x
            ambient_light_uniform.color.y = ambient_light.color.y
            ambient_light_uniform.color.z = ambient_light.color.z

            ambient_light_uniform.energy = 1.0

            self.device.queue.write_buffer(
                self.ambient_light_uniform_buffer,
                0,
                as_capsule(ambient_light_uniform),
                self.ambient_light_uniform_buffer_size,
            )

            super().draw(renderer)
