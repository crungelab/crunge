from typing import Dict
from pathlib import Path

import imageio.v3 as iio
from loguru import logger

from crunge import wgpu
from crunge.wgpu import utils
from crunge.engine import Base

from crunge.engine.resource.texture import Texture


class TextureKitBase(Base):
    def __init__(self):
        super().__init__()
        self.textures: Dict[Path, Texture] = {}
    
    def load_wgpu_texture(self, path: Path) -> Texture:
        im = iio.imread(path, pilmode='RGBA')
        shape = im.shape
        logger.debug(f"shape: {shape}")
        im_height, im_width, im_channels = shape
        im_depth = 1
        # Has to be a multiple of 256
        size = utils.divround_up(im.nbytes, 256)
        logger.debug(f"size: {size}")

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        texture = self.device.create_texture(descriptor)

        bytes_per_row = im_channels * im_width
        logger.debug(f"bytes_per_row: {bytes_per_row}")
        rows_per_image = im_height

        self.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.ImageCopyTexture(
                texture=texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            utils.as_capsule(im),
            # Data size
            size,
            # The layout of the texture
            wgpu.TextureDataLayout(
                offset=0,
                bytes_per_row=bytes_per_row,
                rows_per_image=rows_per_image,
            ),
            # The texture size
            wgpu.Extent3D(im_width, im_height, im_depth),
        )

        return texture, im_width, im_height