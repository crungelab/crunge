from ctypes import (
    Structure,
    c_float,
    c_uint32,
    sizeof,
    c_bool,
    c_int,
    c_void_p,
    cast,
    POINTER,
)

from loguru import logger
import numpy as np
import glm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from .node import Node
from .camera import Camera
from .uniforms import (
    cast_matrix3,
    cast_matrix4,
    cast_vec3,
    CameraUniform,
    LightUniform,
)

class Mesh(Node):
    pipeline: wgpu.RenderPipeline = None
    bind_group: wgpu.BindGroup = None

    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    index_data: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = None

    camera_uniform_buffer: wgpu.Buffer = None
    camera_uniform_buffer_size: int = 0

    light_uniform_buffer: wgpu.Buffer = None
    light_uniform_buffer_size: int = 0

    def __init__(self) -> None:
        super().__init__()
        # Uniform Buffers
        self.camera_uniform_buffer_size = sizeof(CameraUniform)
        self.camera_uniform_buffer = utils.create_buffer(
            self.device,
            "Camera Uniform Buffer",
            self.camera_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        self.light_uniform_buffer_size = sizeof(LightUniform)
        self.light_uniform_buffer = utils.create_buffer(
            self.device,
            "Light Uniform Buffer",
            self.light_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def draw(self, camera: Camera, pass_enc: wgpu.RenderPassEncoder):
        model_matrix = self.transform
        transform_matrix = camera.transform_matrix * self.transform
        normal_matrix = glm.transpose(glm.inverse(glm.mat3(model_matrix)))

        camera_uniform = CameraUniform()
        camera_uniform.model_matrix.data = cast_matrix4(model_matrix)
        camera_uniform.transform_matrix.data = cast_matrix4(transform_matrix)
        camera_uniform.normal_matrix.data = cast_matrix3(normal_matrix)

        #camera_uniform.position.x = camera.position.x
        #camera_uniform.position.y = camera.position.y
        #camera_uniform.position.z = camera.position.z
        camera_uniform.position = cast_vec3(camera.position)

        self.device.queue.write_buffer(
            self.camera_uniform_buffer,
            0,
            camera_uniform
        )

        '''
        self.device.queue.write_buffer(
            self.camera_uniform_buffer,
            0,
            as_capsule(camera_uniform),
            self.camera_uniform_buffer_size,
        )
        '''

        light_uniform = LightUniform()
        
        light_uniform.position.x = 2.0
        light_uniform.position.y = 2.0
        light_uniform.position.z = 2.0
        #light_uniform.position = cast_vec3(glm.vec3(2.0, 2.0, 2.0))

        light_uniform.color.x = 1.0
        light_uniform.color.y = 1.0
        light_uniform.color.z = 1.0

        light_uniform.range = 10.0
        light_uniform.intensity = 10.0

        self.device.queue.write_buffer(
            self.light_uniform_buffer,
            0,
            light_uniform
        )

        '''
        self.device.queue.write_buffer(
            self.light_uniform_buffer,
            0,
            as_capsule(light_uniform),
            self.light_uniform_buffer_size,
        )
        '''

        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        # pass_enc.draw_indexed(len(self.index_data)* 3)
        pass_enc.draw_indexed(len(self.index_data))
