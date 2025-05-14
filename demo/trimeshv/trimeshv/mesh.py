import numpy as np
import glm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from .node import Node
from .camera import Camera

class Mesh(Node):
    pipeline: wgpu.RenderPipeline = None
    bind_group: wgpu.BindGroup = None

    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    index_data: np.ndarray = None
    index_buffer: wgpu.Buffer = None

    uniform_buffer: wgpu.Buffer = None
    uniform_buffer_size: int = 0

    def __init__(self) -> None:
        pass

    def draw(self, camera: Camera, pass_enc: wgpu.RenderPassEncoder):
        transform = camera.transform_matrix

        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            transform
        )

        '''
        self.device.queue.write_buffer(
            self.uniform_buffer,
            0,
            as_capsule(glm.value_ptr(transform)),
            self.uniform_buffer_size,
        )
        '''

        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, wgpu.IndexFormat.UINT32)
        pass_enc.draw_indexed(len(self.index_data)* 3)
