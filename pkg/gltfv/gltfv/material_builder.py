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
        logger.debug(tm_material)
        logger.debug(tm_material.__dict__)
        if tm_material.baseColorTexture:
            texture = TextureBuilder('baseColor').build(tm_material.baseColorTexture)
            self.material.base_color_texture = texture
            self.material.add_texture(texture)

        return self.material