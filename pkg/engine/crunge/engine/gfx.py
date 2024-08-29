import numpy as np
from pathlib import Path
import imageio.v3 as iio

from loguru import logger

from crunge.core import klass
from crunge import wgpu
import crunge.wgpu.utils as utils

from . import globals

@klass.singleton
class Gfx:
    def __init__(self) -> None:
        logger.debug("Creating Gfx")
        self.instance = wgpu.create_instance()
        self.adapter = self.instance.request_adapter()
        self.device = self.adapter.create_device()
        self.device.set_label("Primary Device")
        self.device.enable_logging()
        self.queue = self.device.get_queue()
        globals.set_gfx(self)

    def create_shader_module(self, code: str) -> wgpu.ShaderModule:
        #logger.debug(f"Creating shader module from code: {code}")
        logger.debug(f"Creating shader module")
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

    def load_texture(self, path: Path) -> wgpu.Texture:
        im = iio.imread(path)
        shape = im.shape
        logger.debug(shape)
        im_width = shape[0]
        im_height = shape[1]
        # im_depth = shape[2]
        im_depth = 1
        # Has to be a multiple of 256
        size = utils.divround_up(im.nbytes, 256)
        logger.debug(size)

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        return self.device.create_texture(descriptor)
