from loguru import logger
import numpy as np

from crunge import wgpu

from ..resource import Resource

class Primitive(Resource):
    def __init__(self) -> None:
        super().__init__()
        self.pipeline: wgpu.RenderPipeline = None
        self.bind_group: wgpu.BindGroup = None

        self.vertex_data: np.ndarray = None
        self.vertex_buffer: wgpu.Buffer = None

        self.index_data: np.ndarray = None
        self.index_buffer: wgpu.Buffer = None
        self.index_format: wgpu.IndexFormat = None

