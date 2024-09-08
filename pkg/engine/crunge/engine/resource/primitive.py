from loguru import logger
import numpy as np

from crunge import wgpu

from .resource import Resource

class Primitive(Resource):
    pipeline: wgpu.RenderPipeline = None
    bind_group: wgpu.BindGroup = None

    vertex_data: np.ndarray = None
    vertex_buffer: wgpu.Buffer = None

    index_data: np.ndarray = None
    index_buffer: wgpu.Buffer = None
    index_format: wgpu.IndexFormat = None

    def __init__(self) -> None:
        super().__init__()
