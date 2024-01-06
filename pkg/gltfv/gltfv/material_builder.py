from loguru import logger
import numpy as np

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils
from crunge import gltf

from .debug import debug_texture_info
from .model_builder import ModelBuilder
from .material import Material
from .texture_builder import TextureBuilder
from .texture import Texture


class MaterialBuilder(ModelBuilder):
    material: Material = None

    def __init__(self, tf_model: gltf.Model, tf_material: gltf.Material) -> None:
        super().__init__(tf_model)
        self.tf_material = tf_material
        self.material = Material()

    def build(self) -> None:
        tf_material = self.tf_material
        logger.debug(tf_material)
        material = self.material

        pbr = tf_material.pbr_metallic_roughness
        logger.debug(pbr)

        # Base Color Factor
        base_color_factor = (1, 1, 1, 1) if not pbr.base_color_factor else pbr.base_color_factor
        material.base_color_factor = base_color_factor
        logger.debug(base_color_factor)
        #exit()

        # Base Color Texture
        if pbr.base_color_texture:
            #texture = TextureBuilder('baseColor', self.tf_model, pbr.base_color_texture).build()
            #material.base_color_texture = texture
            #material.add_texture(texture)
            self.build_texture('baseColor', pbr.base_color_texture)

        # Metallic Factor
        metallic_factor = 1 if not pbr.metallic_factor else pbr.metallic_factor
        material.metallic_factor = metallic_factor
        logger.debug(metallic_factor)

        # Roughness Factor
        roughness_factor = 1 if not pbr.roughness_factor else pbr.roughness_factor
        material.roughness_factor = roughness_factor
        logger.debug(roughness_factor)
        #exit()

        # Metallic Roughness Texture
        if pbr.metallic_roughness_texture:
            #texture = TextureBuilder('metallicRoughness', self.tf_model, pbr.metallic_roughness_texture).build()
            #material.metallic_roughness_texure = texture
            #material.add_texture(texture)
            self.build_texture('metallicRoughness', pbr.metallic_roughness_texture)

        # Normal Texture
        if tf_material.normal_texture:
            #texture = TextureBuilder('normal').build(tf_material.normalTexture)
            #material.normal_texure = texture
            #material.add_texture(texture)
            self.build_texture('normal', tf_material.normal_texture)

        # Occlusion Texture
        if tf_material.occlusion_texture:
            #texture = TextureBuilder('occlusion').build(tf_material.occlusionTexture)
            #material.occlusion_texure = texture
            #material.add_texture(texture)
            self.build_texture('occlusion', tf_material.occlusion_texture)

        #emissive_factor = tf_material.emissiveFactor if tf_material.emissiveFactor else (1, 1, 1)
        emissive_factor = (0, 0, 0) if not tf_material.emissive_factor else tf_material.emissive_factor
        material.emissive_factor = emissive_factor
        logger.debug(f"emissive_factor: {emissive_factor}")

        # Emissive Texture
        if tf_material.emissive_texture:
            #texture = TextureBuilder('emissive').build(tf_material.emissiveTexture)
            #material.emissive_texture = texture
            #material.add_texture(texture)
            self.build_texture('emissive', tf_material.emissive_texture)

        return self.material
    
    def build_texture(self, name: str, texture_info: gltf.TextureInfo) -> None:
        debug_texture_info(texture_info)
        if texture_info.index < 0:
            logger.debug(f"texture_info.index < 0: {texture_info.index}")
            return
        texture = TextureBuilder(name, self.tf_model, texture_info).build()
        self.material.add_texture(texture)