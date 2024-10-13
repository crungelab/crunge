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
    LightUniform,
)

from ..resource.mesh import Mesh
from ..resource.primitive import Primitive


class MeshNode3D(Node3D):
    def __init__(self) -> None:
        super().__init__()
        self.mesh: Mesh = None

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
            self.scene.camera_uniform_buffer,
            0,
            as_capsule(camera_uniform),
            self.scene.camera_uniform_buffer_size,
        )

        for primitive in self.mesh.primitives:
            self.draw_primitive(renderer, primitive)

        super().draw(renderer)

    def draw_primitive(self, renderer: Renderer3D, primitive: Primitive):
        pass_enc = renderer.pass_enc

        pass_enc.set_pipeline(primitive.pipeline)
        pass_enc.set_bind_group(0, self.camera_uniform_buffer)
        pass_enc.set_bind_group(1, primitive.bind_group)
        pass_enc.set_vertex_buffer(0, primitive.vertex_buffer)
        pass_enc.set_index_buffer(primitive.index_buffer, primitive.index_format)
        pass_enc.draw_indexed(len(primitive.index_data))