from pathlib import Path
import importlib.resources

from loguru import logger
import numpy as np
import imageio.v3 as iio

from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge import gltf

from crunge.engine import RectI

from crunge.engine.resource.material import Material
from crunge.engine.resource.texture import Texture

from crunge.engine.loader.texture_loader import TextureLoader
from crunge.engine.loader.cube_texture_loader import CubeTextureLoader
from crunge.engine.loader.image_loader import HdrImageLoader

from ..debug import debug_texture_info
from . import GltfBuilder
from .builder_context import BuilderContext
from .texture_builder import TextureBuilder


class MaterialBuilder(GltfBuilder):
    material: Material = None

    def __init__(self, context: BuilderContext, tf_material: gltf.Material) -> None:
        super().__init__(context)
        self.tf_material = tf_material
        self.material = Material()
        self.use_environment_map = False

    def build(self) -> None:
        tf_material = self.tf_material
        logger.debug(tf_material)
        material = self.material

        pbr = tf_material.pbr_metallic_roughness
        logger.debug(pbr)

        # Base Color Factor
        base_color_factor = pbr.base_color_factor
        material.base_color_factor = base_color_factor
        logger.debug(f"Base Color Factor: {base_color_factor}")

        # Base Color Texture
        if pbr.base_color_texture.index >= 0:
            self.build_texture('baseColor', pbr.base_color_texture)

        # Metallic Factor
        metallic_factor = pbr.metallic_factor
        material.metallic_factor = metallic_factor
        logger.debug(f"metallic_factor: {metallic_factor}")

        # Roughness Factor
        roughness_factor = pbr.roughness_factor
        material.roughness_factor = roughness_factor
        logger.debug(f"roughness_factor: {roughness_factor}")

        # Metallic Roughness Texture
        if pbr.metallic_roughness_texture.index >= 0:
            self.build_texture('metallicRoughness', pbr.metallic_roughness_texture)
            self.use_environment_map = True
        # Normal Texture
        if tf_material.normal_texture.index >= 0:
            self.build_texture('normal', tf_material.normal_texture)

        # Occlusion Texture
        if tf_material.occlusion_texture.index >= 0:
            self.occlusion_strength = tf_material.occlusion_texture.strength
            self.build_texture('occlusion', tf_material.occlusion_texture)

        emissive_factor = tf_material.emissive_factor
        material.emissive_factor = emissive_factor
        logger.debug(f"emissive_factor: {emissive_factor}")

        # Emissive Texture
        if tf_material.emissive_texture.index >= 0:
            self.build_texture('emissive', tf_material.emissive_texture)

        if self.use_environment_map:
            self.build_environment_map()

        return self.material
    
    def build_texture(self, name: str, texture_info: gltf.TextureInfo) -> None:
        debug_texture_info(texture_info)
        texture = TextureBuilder(self.context, name, texture_info).build()
        self.material.add_texture(texture)

    def build_environment_map(self) -> None:
        #texture = self.build_environment_texture()
        texture = self.build_cube_environment_texture()
        self.material.add_texture(texture)

    def build_environment_texture(self) -> Texture:
        path = importlib.resources.path('crunge.engine.resources.textures', 'environment.hdr')
        texture = TextureLoader(image_loader=HdrImageLoader()).load(path, name="environment")
        texture.view = texture.texture.create_view()
        texture.sampler = self.gfx.device.create_sampler()
        return texture

    def build_cube_environment_texture(self) -> Texture:
        root = importlib.resources.path('crunge.engine.resources.textures.cubemaps', '')
        #name = "bridge2"
        #ext = "jpg"
        name = "gcanyon_cube"
        ext = "png"
        paths = [
            root / f"{name}_px.{ext}",
            root / f"{name}_nx.{ext}",
            root / f"{name}_py.{ext}",
            root / f"{name}_ny.{ext}",
            root / f"{name}_pz.{ext}",
            root / f"{name}_nz.{ext}",
        ]
        texture = CubeTextureLoader().load(paths, name="environment")
        texture_view_desc = wgpu.TextureViewDescriptor(
            dimension=wgpu.TextureViewDimension.CUBE,
        )
        texture.view = texture.texture.create_view(texture_view_desc)
        texture.sampler = self.gfx.device.create_sampler()
        return texture

    """
    def build_environment_texture(self) -> Texture:
        #path = Path('resources/textures/environment.jpg')
        path = importlib.resources.path('crunge.engine.resources.textures', 'environment.hdr')
        #im = iio.imread(path, pilmode='RGBA')
        #im = iio.imread(path, pilmode='HDR-FI')
        #im = iio.imread(path, format='HDR-FI')
        #im = iio.imread(path, format='opencv')
        im = iio.imread(path)
        #im = np.flipud(im)
        shape = im.shape
        logger.debug(f"im.shape: {shape}")
        logger.debug(f"im.dtype: {im.dtype}")
        logger.debug(f"im.nbytes: {im.nbytes}")
        logger.debug(f"im.size: {im.size}")
        logger.debug(f"im.itemsize: {im.itemsize}")
        logger.debug(f"im.ndim: {im.ndim}")
        logger.debug(f"im.strides: {im.strides}")
        #logger.debug(im)
        im_height, im_width, im_channels = shape
        im_depth = 1

        # Since .hdr files don't have an alpha channel, we manually add it
        if im_channels == 3:
            # Add an alpha channel
            im = np.concatenate([im, np.ones((im_height, im_width, 1), dtype=im.dtype)], axis=-1)

        # Has to be a multiple of 256
        size = utils.divround_up(im.nbytes, 256)
        logger.debug(f"size: {size}")


        descriptor = wgpu.TextureDescriptor(
            dimension = wgpu.TextureDimension.E2D,
            size=wgpu.Extent3D(im_width, im_height, im_depth),
            sample_count = 1,
            format = wgpu.TextureFormat.RGBA8_UNORM,
            #format = wgpu.TextureFormat.RGBA16_FLOAT,
            #format = wgpu.TextureFormat.RGBA32_FLOAT,
            mip_level_count = 1,
            usage=wgpu.TextureUsage.COPY_DST | wgpu.TextureUsage.TEXTURE_BINDING,
        )
        wgpu_texture = self.gfx.device.create_texture(descriptor)
        texture = Texture('environment', RectI(0, 0, im_width, im_height), wgpu_texture)
        texture.view = wgpu_texture.create_view()

        '''
        sampler_desc = wgpu.SamplerDescriptor(
            address_mode_u=wgpu.AddressMode.MIRROR_REPEAT,
            address_mode_v=wgpu.AddressMode.MIRROR_REPEAT,
            address_mode_w=wgpu.AddressMode.MIRROR_REPEAT,
            mag_filter=wgpu.FilterMode.LINEAR,
            min_filter=wgpu.FilterMode.LINEAR,
            mipmap_filter=wgpu.MipmapFilterMode.LINEAR,
            lod_min_clamp=0,
            lod_max_clamp=100,
            compare=wgpu.CompareFunction.UNDEFINED,
            anisotropy=16,
        )
        texture.sampler = self.gfx.device.create_sampler(sampler_desc)
        '''
        texture.sampler = self.gfx.device.create_sampler()
        
        bytes_per_row = 4 * im_width
        #bytes_per_row = 8 * im_width
        #bytes_per_row = 16 * im_width
        #bytes_per_row = 6 * im_width
        #bytes_per_row = 12 * im_width
        logger.debug(f"bytes_per_row: {bytes_per_row}")
        rows_per_image = im_height

        self.gfx.device.queue.write_texture(
            # Tells wgpu where to copy the pixel data
            wgpu.ImageCopyTexture(
                texture=texture.texture,
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
            #The texture size
            wgpu.Extent3D(im_width, im_height, im_depth),
        )
        return texture
    """