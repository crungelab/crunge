from ctypes import Structure, c_float, c_uint32, sizeof, c_bool, c_int, c_void_p, cast, POINTER

import numpy as np
import glm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from .node import Node
from .camera import Camera

# MAT4_SIZE = 4 * 4 * 4


class Vec3(Structure):
    _fields_ = [("x", c_float), ("y", c_float), ("z", c_float)]


class Mat4(Structure):
    _fields_ = [("data", c_float * 16)]  # GLM uses column-major order


class Mat3(Structure):
    _fields_ = [("data", c_float * 9)]  # GLM uses column-major order


class Light(Structure):
    _fields_ = [("position", Vec3), ("color", Vec3), ("intensity", c_float)]


class Uniforms(Structure):
    _fields_ = [("transform_matrix", Mat4), ("normal_matrix", Mat3), ("light", Light)]


'''
ptr = glm.value_ptr(matrix)
ctypes.cast(ptr, ctypes.POINTER(ctypes.c_float * 16)).contents

ptr = glm.value_ptr(matrix)
ctypes.cast(glm.value_ptr(matrix), ctypes.POINTER(ctypes.c_float * 16)).contents
'''
def cast_matrix4(matrix):
    ptr = glm.value_ptr(matrix)
    return cast(ptr, POINTER(c_float * 16)).contents

def cast_matrix3(matrix):
    ptr = glm.value_ptr(matrix)
    return cast(ptr, POINTER(c_float * 9)).contents

class Mesh(Node):
    pipeline: wgpu.RenderPipeline = None
    bind_group: wgpu.BindGroup = None

    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    index_data: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = None

    uniform_buffer: wgpu.Buffer = None
    uniform_buffer_size: int = 0

    def __init__(self) -> None:
        super().__init__()
        # Uniform Buffer

        # uniform_buffer_size = 4 * 16
        self.uniform_buffer_size = sizeof(Uniforms)

        uniform_buffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            self.uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        self.uniform_buffer = uniform_buffer
    
    def draw(self, camera: Camera, pass_enc: wgpu.RenderPassEncoder):
        transform_matrix = camera.transform_matrix
        normal_matrix = glm.transpose(glm.inverse(glm.mat3(transform_matrix)))

        uniforms = Uniforms()
        uniforms.transform_matrix.data = cast_matrix4(transform_matrix)
        uniforms.normal_matrix.data = cast_matrix3(normal_matrix)
        uniforms.light.position.x = 2.0
        uniforms.light.position.y = 4.0
        uniforms.light.position.z = 3.0
        uniforms.light.color.x = 1.0
        uniforms.light.color.y = 1.0
        uniforms.light.color.z = 1.0
        uniforms.light.intensity = 1.0


        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            as_capsule(uniforms),
            self.uniform_buffer_size,
        )

        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        # pass_enc.draw_indexed(len(self.index_data)* 3)
        pass_enc.draw_indexed(len(self.index_data))
