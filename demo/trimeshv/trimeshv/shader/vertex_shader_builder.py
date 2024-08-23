from loguru import logger
import numpy as np
import trimesh as tm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ..vertex_table import VertexTable
from .shader_builder import ShaderBuilder

vertex_shader_code = """
@vertex
fn vs_main(in : VertexInput) -> VertexOutput {
    let vert_pos = uniforms.modelViewProjectionMatrix * in.pos;
"""

'''
return VertexOutput(vert_pos, in.normal, in.uv);
}
'''

class VertexShaderBuilder(ShaderBuilder):
    def __init__(self, vertex_table: VertexTable) -> None:
        super().__init__(vertex_table)
        self(vertex_shader_code)

    def build(self) -> wgpu.ShaderModule :
        logger.debug("Building vertex shader")
        self.build_return()
        super().build()
        #logger.debug(f"vertex_shader_code:\n{self.shader_code}")
        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, self.shader_code
        )
        return shader_module

    def build_return(self):
        self.write('return VertexOutput(vert_pos')
        for column in self.vertex_table.columns:
            if column.name == 'pos':
                continue
            self.write(f', in.{column.name}')
        self.write(');\n')
        self('}')
