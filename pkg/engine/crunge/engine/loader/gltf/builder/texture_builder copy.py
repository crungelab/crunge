from loguru import logger
import glm

from crunge import wgpu
from crunge import gltf

from crunge.engine.resource.texture import Texture

from ..debug import debug_texture, debug_image
from . import GltfBuilder
from .builder_context import BuilderContext
from .sampler_builder import SamplerBuilder
from .image_builder import ImageBuilder

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
        if self.texture_info.index in self.context.texture_cache:
            return self.context.texture_cache[self.texture_info.index]

        tf_texture = self.tf_model.textures[self.texture_info.index]
        #debug_texture(tf_texture)

        im = ImageBuilder(self.context, tf_texture.source).build()
        #tf_image = self.tf_model.images[tf_texture.source]
        #im_width = tf_image.width
        im_width = im.width
        #im_height = tf_image.height
        im_height = im.height
        im_depth = 1

        descriptor = wgpu.TextureDescriptor(
            dimension=wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count=1,
            format=wgpu.TextureFormat.RGBA8_UNORM,
            mip_level_count=1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )

        wgpu_texture = self.gfx.device.create_texture(descriptor)
        self.texture = Texture(wgpu_texture, glm.ivec3(im_width, im_height, im_depth)).set_name(
            self.name
        )
        self.texture.view = wgpu_texture.create_view()

        self.texture.sampler = SamplerBuilder(self.context, tf_texture.sampler).build().sampler

        bytes_per_row = 4 * im_width
        logger.debug(f"bytes_per_row: {bytes_per_row}")
        rows_per_image = im_height

        self.gfx.device.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.TexelCopyTextureInfo(
                texture=self.texture.texture,
                mip_level=0,
                origin=wgpu.Origin3D(0, 0, 0),
                aspect=wgpu.TextureAspect.ALL,
            ),
            # The actual pixel data
            im.data,
            # The layout of the texture
            wgpu.TexelCopyBufferLayout(
                offset=0,
                bytes_per_row=bytes_per_row,
                rows_per_image=rows_per_image,
            ),
            # The texture size
            wgpu.Extent3D(im_width, im_height, im_depth),
        )

        self.context.texture_cache[self.texture_info.index] = self.texture
        return self.texture
