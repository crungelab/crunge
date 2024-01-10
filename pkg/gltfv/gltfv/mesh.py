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
    VsUniforms,
    FsUniforms,
)

class Mesh(Node):
    pipeline: wgpu.RenderPipeline = None
    bind_group: wgpu.BindGroup = None

    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    index_data: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = None

    vs_uniform_buffer: wgpu.Buffer = None
    vs_uniform_buffer_size: int = 0

    fs_uniform_buffer: wgpu.Buffer = None
    fs_uniform_buffer_size: int = 0

    def __init__(self) -> None:
        super().__init__()
        # Uniform Buffers
        self.vs_uniform_buffer_size = sizeof(VsUniforms)
        self.vs_uniform_buffer = utils.create_buffer(
            self.device,
            "Vertex Uniform Buffer",
            self.vs_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        self.fs_uniform_buffer_size = sizeof(FsUniforms)
        self.fs_uniform_buffer = utils.create_buffer(
            self.device,
            "Fragment Uniform Buffer",
            self.fs_uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )

    def draw(self, camera: Camera, pass_enc: wgpu.RenderPassEncoder):
        transform_matrix = camera.transform_matrix * self.transform
        normal_matrix = glm.transpose(glm.inverse(glm.mat3(transform_matrix)))

        vs_uniforms = VsUniforms()
        vs_uniforms.transform_matrix.data = cast_matrix4(transform_matrix)
        vs_uniforms.normal_matrix.data = cast_matrix3(normal_matrix)

        self.device.queue.write_buffer(
            self.vs_uniform_buffer,
            0,
            as_capsule(vs_uniforms),
            self.vs_uniform_buffer_size,
        )

        fs_uniforms = FsUniforms()
        
        #fs_uniforms.light.position.x = -2.0
        #fs_uniforms.light.position.y = 4.0
        #fs_uniforms.light.position.z = 3.0
        fs_uniforms.light.position.data = cast_vec3(glm.vec3(2.0, 4.0, 3.0))

        fs_uniforms.light.color.x = 1.0
        fs_uniforms.light.color.y = 1.0
        fs_uniforms.light.color.z = 1.0
        fs_uniforms.light.intensity = 5.0

        #fs_uniforms.camera.position.x = camera.position.x
        #fs_uniforms.camera.position.y = camera.position.y
        #fs_uniforms.camera.position.z = camera.position.z
        fs_uniforms.camera.position.data = cast_vec3(camera.position)

        self.device.queue.write_buffer(
            self.fs_uniform_buffer,
            0,
            as_capsule(fs_uniforms),
            self.fs_uniform_buffer_size,
        )

        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        # pass_enc.draw_indexed(len(self.index_data)* 3)
        pass_enc.draw_indexed(len(self.index_data))
