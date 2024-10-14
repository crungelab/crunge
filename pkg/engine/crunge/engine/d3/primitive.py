from loguru import logger
import numpy as np

from crunge import wgpu

from .renderer_3d import Renderer3D


class Primitive:
    pipeline: wgpu.RenderPipeline = None

    #camera_bind_group: wgpu.BindGroup = None
    light_bind_group: wgpu.BindGroup = None
    material_bind_group: wgpu.BindGroup = None
    model_bind_group: wgpu.BindGroup = None

    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    index_data: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = None

    def __init__(self) -> None:
        super().__init__()

    def draw(self, renderer: Renderer3D):
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.pipeline)

        #pass_enc.set_bind_group(0, self.camera_bind_group)
        pass_enc.set_bind_group(1, self.light_bind_group)
        pass_enc.set_bind_group(2, self.material_bind_group)
        pass_enc.set_bind_group(3, self.model_bind_group)

        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        pass_enc.draw_indexed(len(self.index_data))
