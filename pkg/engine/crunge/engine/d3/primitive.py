from loguru import logger
import numpy as np

from crunge import wgpu

from ..resource.material import Material

from .renderer_3d import Renderer3D
from .program_3d import Program3D
from .material_3d import Material3D

class PrimitiveProgram(Program3D):
    pipeline: wgpu.RenderPipeline = None


class Primitive:
    #pipeline: wgpu.RenderPipeline = None
    program: PrimitiveProgram = None
    material: Material = None

    #camera_bind_group: wgpu.BindGroup = None
    #light_bind_group: wgpu.BindGroup = None
    #material_bind_group: wgpu.BindGroup = None
    #model_bind_group: wgpu.BindGroup = None

    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    index_data: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = None

    def __init__(self) -> None:
        super().__init__()

    def draw(self, renderer: Renderer3D):
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.pipeline)
        self.material.bind(pass_enc)

        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        pass_enc.draw_indexed(len(self.index_data))
