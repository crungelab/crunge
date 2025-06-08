from loguru import logger

from crunge import wgpu

from crunge.engine.resource.texture.cube_texture import CubeTexture
from crunge.engine.d3.material_3d import Material3D

from ..vertex_table import VertexTable
from ..builder_context import BuilderContext
from .shader_builder import ShaderBuilder

MATERIAL_GROUP_INDEX = 2

class Binding:
    def __init__(self, name: str, type: str, index: int, group: int) -> None:
        self.name = name
        self.type = type
        self.index = index
        self.group = group

class FragmentShaderBuilder(ShaderBuilder):
    def __init__(self, context: BuilderContext, vertex_table: VertexTable, material: Material3D) -> None:
        super().__init__(context, vertex_table)
        self.material = material
        self.bindings: list[Binding] = []

        self.base_color_factor = material.base_color_factor
        self.metallic_factor = material.metallic_factor
        self.roughness_factor = material.roughness_factor
        self.occlusion_strength = material.occlusion_strength
        self.emissive_factor = material.emissive_factor
        self.alpha_mode = material.alpha_mode
        self.alpha_cutoff = material.alpha_cutoff

    def add_binding(self, binding: Binding):
        self.bindings.append(binding)
    
    def build(self) -> wgpu.ShaderModule :
        super().build()
        logger.debug("Building fragment shader")
        material = self.material

        for i, texture in enumerate(material.textures):
            texture_type = 'texture_2d<f32>'
            if isinstance(texture, CubeTexture):
                texture_type = 'texture_cube<f32>'

            self.add_binding(Binding(f'{texture.name}Sampler', 'sampler', i * 2, MATERIAL_GROUP_INDEX))
            self.add_binding(Binding(f'{texture.name}Texture', texture_type, i * 2 + 1, MATERIAL_GROUP_INDEX))

        shader_code = self.generate('fragment.wgsl')
        #logger.debug(f"fragment_shader_code:\n{shader_code}")

        shader_module: wgpu.ShaderModule = self.gfx.create_shader_module(shader_code)

        return shader_module
