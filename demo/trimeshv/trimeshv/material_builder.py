from loguru import logger
import numpy as np
import trimesh as tm

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

    def build(self, tm_material) -> Material:
        material = self.material
        logger.debug(tm_material)
        logger.debug(tm_material.__dict__)

        # Base Color Factor
        base_color_factor = (1, 1, 1, 1) if tm_material.baseColorFactor is None else tm_material.baseColorFactor
        material.base_color_factor = base_color_factor
        logger.debug(base_color_factor)

        # Base Color Texture
        if tm_material.baseColorTexture is not None:
            texture = TextureBuilder('baseColor').build(tm_material.baseColorTexture)
            material.add_texture(texture)

        # Metallic Factor
        metallic_factor = 1 if tm_material.metallicFactor is None else tm_material.metallicFactor
        material.metallic_factor = metallic_factor
        logger.debug(metallic_factor)

        # Roughness Factor
        roughness_factor = 1 if tm_material.roughnessFactor is None else tm_material.roughnessFactor
        material.roughness_factor = roughness_factor
        logger.debug(roughness_factor)

        # Metallic Roughness Texture
        if tm_material.metallicRoughnessTexture is not None:
            texture = TextureBuilder('metallicRoughness').build(tm_material.metallicRoughnessTexture)
            material.add_texture(texture)

        # Normal Texture
        if tm_material.normalTexture is not None:
            texture = TextureBuilder('normal').build(tm_material.normalTexture)
            material.add_texture(texture)

        # Occlusion Texture
        if tm_material.occlusionTexture is not None:
            texture = TextureBuilder('occlusion').build(tm_material.occlusionTexture)
            material.add_texture(texture)

        emissive_factor = (0, 0, 0) if tm_material.emissiveFactor is None else tm_material.emissiveFactor
        material.emissive_factor = emissive_factor
        logger.debug(f"emissive_factor: {emissive_factor}")

        # Emissive Texture
        if tm_material.emissiveTexture:
            texture = TextureBuilder('emissive').build(tm_material.emissiveTexture)
            material.add_texture(texture)

        return self.material