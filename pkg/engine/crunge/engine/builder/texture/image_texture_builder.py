from typing import TYPE_CHECKING, Dict, List
from typing import List
from pathlib import Path

from loguru import logger

from crunge import wgpu
from crunge.wgpu import utils

from ..resource_builder import ResourceBuilder

from ...resource.resource_manager import ResourceManager
from ...resource.texture import ImageTexture, TextureKit
from ...resource.image import Image

from .texture_builder import TextureBuilder


class ImageTextureBuilder(TextureBuilder[ImageTexture]):
    def __init__(self, kit: TextureKit = ResourceManager().texture_kit) -> None:
        super().__init__(kit)

    def build(self, image: Image) -> ImageTexture:
        wgpu_texture = self.build_wpgu_texture(image)
        return (
            ImageTexture(wgpu_texture, image.size, image)
            .set_name(image.name)
            .set_path(image.path)
        )

    def build_wpgu_texture(self, image: Image) -> ImageTexture:
        #logger.debug(f"Building ImageTexture: {image.name}")
        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(image.width, image.height, 1),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        texture = self.device.create_texture(descriptor)

        im = image.data
        shape = im.shape
        # logger.debug(f"shape: {shape}")
        im_height, im_width, im_channels = shape
        im_depth = 1
        # Has to be a multiple of 256
        size = utils.divround_up(im.nbytes, 256)
        # logger.debug(f"size: {size}")

        bytes_per_row = im_channels * im_width
        # logger.debug(f"bytes_per_row: {bytes_per_row}")
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

        return texture
