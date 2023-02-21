from loguru import logger
import numpy as np
import trimesh as tm

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

    def build(self, tm_material) -> Material:
        material = self.material
        logger.debug(tm_material)
        logger.debug(tm_material.__dict__)

        # Base Color Factor
        base_color_factor = tm_material.baseColorFactor
        if not base_color_factor:
            base_color_factor = (1, 1, 1, 1)
        material.base_color_factor = base_color_factor
        logger.debug(base_color_factor)
        #exit()

        # Base Color Texture
        if tm_material.baseColorTexture:
            texture = TextureBuilder('baseColor').build(tm_material.baseColorTexture)
            material.base_color_texture = texture
            material.add_texture(texture)

        # Metallic Factor
        metallic_factor = tm_material.metallicFactor
        if not metallic_factor:
            metallic_factor = 1
        material.metallic_factor = metallic_factor
        logger.debug(metallic_factor)

        # Roughness Factor
        roughness_factor = tm_material.roughnessFactor
        if not roughness_factor:
            roughness_factor = 1
        material.roughness_factor = roughness_factor
        logger.debug(roughness_factor)
        #exit()

        # Metallic Roughness Texture
        if tm_material.metallicRoughnessTexture:
            texture = TextureBuilder('metallicRoughness').build(tm_material.metallicRoughnessTexture)
            material.metallic_roughness_texure = texture
            material.add_texture(texture)

        # Metallic Roughness Texture
        if tm_material.normalTexture:
            texture = TextureBuilder('normal').build(tm_material.normalTexture)
            material.normal_texure = texture
            material.add_texture(texture)

        return self.material