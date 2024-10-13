from loguru import logger
import numpy as np

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge import gltf

from crunge.engine.math import Rect2i
from crunge.engine.resource.texture import Texture

from ..debug import debug_texture, debug_image
from . import GltfBuilder
from .builder_context import BuilderContext


class TextureBuilder(GltfBuilder):
    name: str = None
    texture: Texture = None

    def __init__(
        self, context: BuilderContext, name: str, texture_info: gltf.TextureInfo
    ) -> None:
        super().__init__(context)
        self.name = name
        self.texture_info = texture_info
        self.texture: Texture = None

    def build(self) -> Texture:
        tf_texture = self.tf_model.textures[self.texture_info.index]
        debug_texture(tf_texture)

        tf_image = self.tf_model.images[tf_texture.source]
        debug_image(tf_image)

        # This was too slow.
        # im = np.array(tf_image.image, dtype=np.uint8)
        # im = np.array(tf_image.image, dtype=np.uint8, copy=False)

        im = tf_image.get_array()

        shape = im.shape
        logger.debug(f"im.shape: {shape}")
        logger.debug(f"im.dtype: {im.dtype}")
        logger.debug(f"im.nbytes: {im.nbytes}")
        logger.debug(f"im.size: {im.size}")
        logger.debug(f"im.itemsize: {im.itemsize}")
        logger.debug(f"im.ndim: {im.ndim}")
        logger.debug(f"im.strides: {im.strides}")
        # logger.debug(im)

        # im_width = shape[0]
        im_width = tf_image.width
        # im_height = shape[1]
        im_height = tf_image.height
        im_depth = 1
        # Has to be a multiple of 256
        size = utils.divround_up(im.nbytes, 256)
        logger.debug(f"im.size: {size}")

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        wgpu_texture = self.gfx.device.create_texture(descriptor)
        self.texture = Texture(wgpu_texture, Rect2i(0, 0, im_width, im_height)).set_name(
            self.name
        )
        self.texture.view = wgpu_texture.create_view()

        sampler_desc = wgpu.SamplerDescriptor(
            address_mode_u=wgpu.AddressMode.REPEAT,
            address_mode_v=wgpu.AddressMode.REPEAT,
            address_mode_w=wgpu.AddressMode.REPEAT,
            mag_filter=wgpu.FilterMode.LINEAR,
            min_filter=wgpu.FilterMode.LINEAR,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            lod_min_clamp=0,
            lod_max_clamp=100,
            compare=wgpu.CompareFunction.UNDEFINED,
            anisotropy=16,
        )

        self.texture.sampler = self.gfx.device.create_sampler(sampler_desc)

        bytes_per_row = 4 * im_width
        logger.debug(f"bytes_per_row: {bytes_per_row}")
        rows_per_image = im_height

        self.gfx.device.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.ImageCopyTexture(
                texture=self.texture.texture,
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
        # exit()
        return self.texture
