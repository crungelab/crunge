import numpy as np
import glm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from .node import Node
from .camera import Camera

MAT4_SIZE = 4 * 4 * 4

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

        #uniform_buffer_size = 4 * 16
        uniform_buffer_size = MAT4_SIZE * 2
        self.uniform_buffer_size = uniform_buffer_size

        uniform_buffer = utils.create_buffer(
            self.device,
            "Uniform buffer",
            uniform_buffer_size,
            wgpu.BufferUsage.UNIFORM,
        )
        self.uniform_buffer = uniform_buffer


    def draw(self, camera: Camera, pass_enc: wgpu.RenderPassEncoder):
        transform_matrix = camera.transform_matrix
        normal_matrix = glm.transpose(glm.inverse(glm.mat3(transform_matrix)))

        uniform_offset = 0

        self.device.queue.write_buffer(
            self.uniform_buffer,
            #0,
            uniform_offset,
            as_capsule(glm.value_ptr(transform_matrix)),
            #self.uniform_buffer_size,
            MAT4_SIZE
        )
        uniform_offset += MAT4_SIZE

        self.device.queue.write_buffer(
            self.uniform_buffer,
            uniform_offset,
            as_capsule(glm.value_ptr(normal_matrix)),
            #self.uniform_buffer_size,
            MAT4_SIZE
        )

        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        #pass_enc.draw_indexed(len(self.index_data)* 3)
        pass_enc.draw_indexed(len(self.index_data))
