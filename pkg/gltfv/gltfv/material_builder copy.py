from loguru import logger
import numpy as np

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from .builder import Builder
from .material import Material
from .texture_builder import TextureBuilder
from .texture import Texture


class MaterialBuilder(Builder):
    material: Material = None

    def __init__(self) -> None:
        self.material = Material()

    def build(self, tf_material) -> Material:
        material = self.material
        logger.debug(tf_material)
        logger.debug(tf_material.__dict__)

        # Base Color Factor
        base_color_factor = (1, 1, 1, 1) if tf_material.baseColorFactor is None else tf_material.baseColorFactor
        material.base_color_factor = base_color_factor
        logger.debug(base_color_factor)
        #exit()

        # Base Color Texture
        if tf_material.baseColorTexture:
            texture = TextureBuilder('baseColor').build(tf_material.baseColorTexture)
            #material.base_color_texture = texture
            material.add_texture(texture)

        # Metallic Factor
        metallic_factor = 1 if tf_material.metallicFactor is None else tf_material.metallicFactor
        material.metallic_factor = metallic_factor
        logger.debug(metallic_factor)

        # Roughness Factor
        roughness_factor = 1 if tf_material.roughnessFactor is None else tf_material.roughnessFactor
        material.roughness_factor = roughness_factor
        logger.debug(roughness_factor)
        #exit()

        # Metallic Roughness Texture
        if tf_material.metallicRoughnessTexture:
            texture = TextureBuilder('metallicRoughness').build(tf_material.metallicRoughnessTexture)
            #material.metallic_roughness_texure = texture
            material.add_texture(texture)

        # Normal Texture
        if tf_material.normalTexture:
            texture = TextureBuilder('normal').build(tf_material.normalTexture)
            #material.normal_texure = texture
            material.add_texture(texture)

        # Occlusion Texture
        if tf_material.occlusionTexture:
            texture = TextureBuilder('occlusion').build(tf_material.occlusionTexture)
            #material.occlusion_texure = texture
            material.add_texture(texture)

        #emissive_factor = tf_material.emissiveFactor if tf_material.emissiveFactor else (1, 1, 1)
        emissive_factor = (0, 0, 0) if tf_material.emissiveFactor is None else tf_material.emissiveFactor
        material.emissive_factor = emissive_factor
        logger.debug(f"emissive_factor: {emissive_factor}")

        # Emissive Texture
        if tf_material.emissiveTexture:
            texture = TextureBuilder('emissive').build(tf_material.emissiveTexture)
            #material.emissive_texture = texture
            material.add_texture(texture)

        return self.material