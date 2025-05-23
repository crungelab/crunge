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
        '''
        instance_capabilities = wgpu.InstanceCapabilities()
        instance_capabilities.timed_wait_any_enable = True

        instance_descriptor = wgpu.InstanceDescriptor()
        instance_descriptor.capabilities = instance_capabilities
        self.instance = wgpu.create_instance(instance_descriptor)
        '''
        #self.instance = wgpu.create_instance()
        #self.instance = utils.create_instance()

        #self.adapter = self.instance.request_adapter()
        #self.adapter = utils.request_adapter(self.instance)

        #self.device = utils.create_device(self.adapter)
        #self.device = self.adapter.create_device()
        self.context = wgpu.Context()
        #self.instance = self.context.instance
        #self.adapter = self.context.adapter
        #self.device = self.context.device
        #self.queue = self.context.queue

        #self.device.set_label("Primary Device")
        #self.device.enable_logging()
        #self.queue = self.device.get_queue()
        globals.set_gfx(self)

    @property
    def instance(self) -> wgpu.Instance:
        return self.context.instance
    
    @property
    def adapter(self) -> wgpu.Adapter:
        return self.context.adapter
    
    @property
    def device(self) -> wgpu.Device:
        return self.context.device
    
    @property
    def queue(self) -> wgpu.Queue:
        return self.context.queue

    def create_shader_module(self, code: str) -> wgpu.ShaderModule:
        #logger.debug(f"Creating shader module from code: {code}")
        logger.debug(f"Creating shader module")
        #wgsl_desc = wgpu.ShaderModuleWGSLDescriptor(code=code)
        wgsl_desc = wgpu.ShaderSourceWGSL(code=code)
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

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        return self.device.create_texture(descriptor)
