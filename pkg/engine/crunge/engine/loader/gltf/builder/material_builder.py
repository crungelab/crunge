from pathlib import Path
import importlib.resources

from loguru import logger
import numpy as np
import imageio.v3 as iio

from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge import gltf

from crunge.engine.math import Rect2i

from crunge.engine.resource.material import Material
from crunge.engine.resource.texture import Texture
from crunge.engine.resource.cube_texture import CubeTexture

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

        self.build_bind_group_layout()
        self.build_bind_group()

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

    def build_bind_group_layout(self) -> wgpu.BindGroupLayout:
        material_bgl_entries = []

        for i, texture in enumerate(self.material.textures):
            view_dimension = wgpu.TextureViewDimension.E2D
            if isinstance(texture, CubeTexture):
                view_dimension = wgpu.TextureViewDimension.CUBE

            # Sampler
            material_bgl_entries.append(
                wgpu.BindGroupLayoutEntry(
                    binding=i * 2,
                    visibility=wgpu.ShaderStage.FRAGMENT,
                    sampler=wgpu.SamplerBindingLayout(
                        type=wgpu.SamplerBindingType.FILTERING
                    ),
                )
            )

            # Texture
            material_bgl_entries.append(
                wgpu.BindGroupLayoutEntry(
                    binding=i * 2 + 1,
                    visibility=wgpu.ShaderStage.FRAGMENT,
                    texture=wgpu.TextureBindingLayout(
                        sample_type=wgpu.TextureSampleType.FLOAT,
                        view_dimension=view_dimension,
                    ),
                )
            )

        material_bgl_desc = wgpu.BindGroupLayoutDescriptor(
            entry_count=len(material_bgl_entries), entries=material_bgl_entries
        )
        material_bgl = self.device.create_bind_group_layout(material_bgl_desc)
        self.material.bind_group_layout = material_bgl

    def build_bind_group(self) -> wgpu.BindGroup:
        material_bg_entries = []
        for i, texture in enumerate(self.material.textures):
            material_bg_entries.append(
                wgpu.BindGroupEntry(
                    binding=i * 2, sampler=texture.sampler
                )
            )
            material_bg_entries.append(
                wgpu.BindGroupEntry(
                    binding=i * 2 + 1, texture_view=texture.view
                )
            )

        material_bg_desc = wgpu.BindGroupDescriptor(
            label="Material Bind Group",
            layout=self.material.bind_group_layout,
            entry_count=len(material_bg_entries),
            entries=material_bg_entries,
        )

        self.material.bind_group = self.device.create_bind_group(material_bg_desc)
