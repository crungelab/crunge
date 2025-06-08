from loguru import logger
import numpy as np
import trimesh as tm

from crunge import wgpu
from crunge.wgpu import utils

from .builder import Builder
from .texture import Texture


class TextureBuilder(Builder):
    name: str = None
    texture: Texture = None

    def __init__(self, name: str) -> None:
        self.texture = Texture(name)

    def build(self, image):
        im = None
        logger.debug(f'image mode: {image.mode}')
        if image.mode != 'RGBA':
            im = np.array(image.convert('RGBA'))
        else:
            im = np.array(image)
        shape = im.shape
        logger.debug(shape)
        im_width = shape[0]
        im_height = shape[1]
        im_depth = 1

        descriptor = wgpu.TextureDescriptor(
            dimension = wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count = 1,
            format = wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count = 1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        wgpu_texture = self.device.create_texture(descriptor)
        self.texture.texture = wgpu_texture
        self.texture.view = wgpu_texture.create_view()

        sampler_desc = wgpu.SamplerDescriptor(
            address_mode_u=wgpu.AddressMode.REPEAT,
            address_mode_v=wgpu.AddressMode.REPEAT,
            address_mode_w=wgpu.AddressMode.REPEAT,
            mag_filter=wgpu.FilterMode.LINEAR,
            min_filter=wgpu.FilterMode.LINEAR,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
        )

        self.texture.sampler = self.device.create_sampler(sampler_desc)
        
        bytes_per_row = 4 * im_width
        logger.debug(bytes_per_row)
        rows_per_image = im_height

        self.device.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.TexelCopyTextureInfo(
                texture=self.texture.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            im,
            # The layout of the texture
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=bytes_per_row,
                rows_per_image=rows_per_image,
            ),
            #The texture size
            wgpu.Extent3D(im_width, im_height, im_depth),
        )

        return self.texture