from textwrap import dedent

from loguru import logger

from crunge import wgpu
import crunge.wgpu.utils as utils

from ..constants import TEXTURE_BINDING_START
from ..vertex_table import VertexTable
from ..material import Material
from .shader_builder import ShaderBuilder


class Binding:
    def __init__(self, name: str, type: str, index: int, group: int) -> None:
        self.name = name
        self.type = type
        self.index = index
        self.group = group

class FragmentShaderBuilder(ShaderBuilder):
    def __init__(self, vertex_table: VertexTable, material: Material) -> None:
        super().__init__(vertex_table)
        self.material = material
        self.bindings: list[Binding] = []

        self.base_color_factor = material.base_color_factor
        self.metallic_factor = material.metallic_factor
        self.roughness_factor = material.roughness_factor
        self.emissive_factor = material.emissive_factor

    def add_binding(self, binding: Binding):
        self.bindings.append(binding)
    
    def build(self) -> wgpu.ShaderModule :
        super().build()
        logger.debug("Building fragment shader")
        material = self.material
        for i, texture in enumerate(material.textures):
            self.add_binding(Binding(f'{texture.name}Sampler', 'sampler', i*2+TEXTURE_BINDING_START, 0))
            self.add_binding(Binding(f'{texture.name}Texture', 'texture_2d<f32>', i*2+TEXTURE_BINDING_START+1, 0))

        shader_code = self.generate('pbr.frag.wgsl')
        logger.debug(f"fragment_shader_code:\n{shader_code}")

        #exit()
        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, shader_code
        )
        #exit()
        return shader_module
