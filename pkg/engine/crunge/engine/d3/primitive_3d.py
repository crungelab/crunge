from loguru import logger
import numpy as np

from crunge import wgpu

from ..math.bounds3 import Bounds3
from ..renderer import Renderer
from ..resource.mesh.primitive import Primitive

from .material_3d import Material3D

from .program_3d import Program3D


class Primitive3DProgram(Program3D):
    def __init__(self):
        super().__init__()
        self.pipeline: wgpu.RenderPipeline = None


class Primitive3D(Primitive):
    def __init__(self) -> None:
        super().__init__()
        self.bounds = Bounds3()
        self.program: Primitive3DProgram = None
        self.material: Material3D = None

    def draw(self, renderer: Renderer):
        pass_enc = renderer.pass_enc
        pass_enc.set_pipeline(self.program.pipeline)
        self.material.bind(pass_enc)

        pass_enc.set_vertex_buffer(0, self.vertex_buffer)
        pass_enc.set_index_buffer(self.index_buffer, self.index_format)
        pass_enc.draw_indexed(len(self.index_data))
