from loguru import logger
import numpy as np

from crunge import wgpu

from .scene_renderer_3d import SceneRenderer3D


class Primitive:
    pipeline: wgpu.RenderPipeline = None
    bind_group: wgpu.BindGroup = None

    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    index_data: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = None

    def __init__(self) -> None:
        super().__init__()

    def draw(self, renderer: SceneRenderer3D):
        pass_enc = renderer.pass_enc

        pass_enc.set_pipeline(self.pipeline)
        pass_enc.set_bind_group(0, self.bind_group)
        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        pass_enc.draw_indexed(len(self.index_data))
