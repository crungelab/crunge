from typing import List

from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import as_capsule
from crunge import wgpu

from .renderer_3d import Renderer3D
from .node_3d import Node3D
from .uniforms_3d import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    CameraUniform,
    ModelUniform,
)
from .primitive import Primitive


class MeshInstance3D(Node3D):
    def __init__(self) -> None:
        super().__init__()
        self.primitives: List[Primitive] = []

        # Uniform Buffers
        self.model_uniform_buffer_size = sizeof(ModelUniform)
        self.model_uniform_buffer = self.gfx.create_buffer(
            "Model Uniform Buffer",
            self.model_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

        '''
        self.camera_uniform_buffer_size = sizeof(CameraUniform)
        self.camera_uniform_buffer = self.gfx.create_buffer(
            "Camera Uniform Buffer",
            self.camera_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        '''

    def add_primitive(self, primitive: Primitive):
        self.primitives.append(primitive)

    def draw(self, renderer: Renderer3D):
        camera = renderer.camera

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
        '''
        camera_uniform = CameraUniform()
        camera_uniform.transform_matrix.data = cast_matrix4(transform_matrix)

        # camera_uniform.position.x = camera.position.x
        # camera_uniform.position.y = camera.position.y
        # camera_uniform.position.z = camera.position.z
        camera_uniform.position = cast_vec3(camera.position)
        #logger.debug(f"camera_uniform.position: {camera_uniform.position.x}, {camera_uniform.position.y}, {camera_uniform.position.z}")

        self.device.queue.write_buffer(
            self.camera_uniform_buffer,
            0,
            as_capsule(camera_uniform),
            self.camera_uniform_buffer_size,
        )
        '''

        for primitive in self.primitives:
            primitive.draw(renderer)

        super().draw(renderer)


    '''
    def draw(self, renderer: Renderer3D):
        camera = renderer.camera

        model_matrix = self.transform
        transform_matrix = camera.transform_matrix * self.transform
        #normal_matrix = glm.transpose(glm.inverse(glm.mat3(model_matrix)))
        normal_matrix = glm.mat4(glm.transpose(glm.inverse(glm.mat3(model_matrix))))

        camera_uniform = CameraUniform()
        camera_uniform.model_matrix.data = cast_matrix4(model_matrix)
        camera_uniform.transform_matrix.data = cast_matrix4(transform_matrix)
        #camera_uniform.normal_matrix.data = cast_matrix3(normal_matrix)
        camera_uniform.normal_matrix.data = cast_matrix4(normal_matrix)

        # camera_uniform.position.x = camera.position.x
        # camera_uniform.position.y = camera.position.y
        # camera_uniform.position.z = camera.position.z
        camera_uniform.position = cast_vec3(camera.position)
        #logger.debug(f"camera_uniform.position: {camera_uniform.position.x}, {camera_uniform.position.y}, {camera_uniform.position.z}")

        self.device.queue.write_buffer(
            self.camera_uniform_buffer,
            0,
            as_capsule(camera_uniform),
            self.camera_uniform_buffer_size,
        )

        for primitive in self.primitives:
            primitive.draw(renderer)

        super().draw(renderer)
        '''