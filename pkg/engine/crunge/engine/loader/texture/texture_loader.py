from typing import TYPE_CHECKING, TypeVar, Generic, Dict, List
from typing import List
from pathlib import Path

from loguru import logger

from crunge import wgpu
from crunge.wgpu import utils

from ..resource_loader import ResourceLoader
from ..image.image_loader import ImageLoader

from ...resource.resource_manager import ResourceManager
from ...resource.texture import Texture, TextureKit
from ...resource.image import Image


T_Resource = TypeVar("T_Resource", bound=Texture)


class TextureDetails:
    def __init__(self, texture: wgpu.Texture, width: int, height: int, depth: int) -> None:
        self.texture = texture
        self.width = width
        self.height = height
        self.depth = depth


class TextureLoader(ResourceLoader[T_Resource]):
    def __init__(
        self,
        kit: TextureKit = ResourceManager().texture_kit,
        image_loader=ImageLoader(),
    ) -> None:
        super().__init__(kit)
        self.image_loader = image_loader

    def load_wgpu_texture(self, paths: List[Path]) -> TextureDetails:
        images: List[Image] = []

        for path in paths:
            image = self.image_loader.load(path)
            images.append(image)

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(images[0].width, images[0].height, len(images)),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        texture = self.device.create_texture(descriptor)

        for i, image in enumerate(images):
            im = image.data
            shape = im.shape
            # logger.debug(f"shape: {shape}")
            im_height, im_width, im_channels = shape
            im_depth = 1

            bytes_per_row = im_channels * im_width
            # logger.debug(f"bytes_per_row: {bytes_per_row}")
            rows_per_image = im_height

            self.queue.write_texture(
                # Tells wgpu where to copy the pixel data
                wgpu.TexelCopyTextureInfo(
                    texture=texture,
                    mip_level=0,
                    origin=wgpu.Origin3D(0, 0, i),
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
                # The texture size
                wgpu.Extent3D(im_width, im_height, im_depth),
            )

        return TextureDetails(texture, im_width, im_height, len(images))
