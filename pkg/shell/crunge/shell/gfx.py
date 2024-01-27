import numpy as np

from loguru import logger

from crunge import wgpu
import crunge.wgpu.utils as utils

from .utils import singleton


@singleton
class Gfx:
    def __init__(self) -> None:
        self.instance = wgpu.create_instance()
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        self.device.set_label("Primary Device")
        self.device.enable_logging()
        self.queue = self.device.get_queue()

    def create_shader_module(self, code: str) -> wgpu.ShaderModule:
        wgsl_desc = wgpu.ShaderModuleWGSLDescriptor(code=code)
        sm_descriptor = wgpu.ShaderModuleDescriptor(next_in_chain=wgsl_desc)
        shader_module = self.device.create_shader_module(sm_descriptor)
        return shader_module

    def create_buffer(self, size: int, usage: wgpu.BufferUsage, data: bytes = None) -> wgpu.Buffer:
        return utils.create_buffer(self.device, size, usage, data)
    
    def create_buffer_from_ndarray(
        self, label: str, data: np.ndarray, usage: wgpu.BufferUsage
    ) -> wgpu.Buffer:
        return utils.create_buffer_from_ndarray(self.device, label, data, usage)
