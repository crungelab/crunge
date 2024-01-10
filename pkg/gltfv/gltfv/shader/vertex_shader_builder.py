from loguru import logger
import numpy as np

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from ..vertex_table import VertexTable
from .shader_builder import ShaderBuilder


vertex_shader_code = """
struct VsUniforms {
    transformMatrix : mat4x4<f32>,
    normalMatrix: mat3x3<f32>,
}
@group(0) @binding(0) var<uniform> uniforms : VsUniforms;

@vertex
fn vs_main(input : VertexInput) -> VertexOutput {
    var output : VertexOutput;
    output.vertex_pos = uniforms.transformMatrix * input.pos;
    output.normal = normalize(((uniforms.transformMatrix * vec4(input.normal.xyz, 0.0))).xyz);
"""
#output.tangent = normalize(((uniforms.transformMatrix * vec4(input.tangent.xyz, 0.0))).xyz);

#output.normal = normalize(uniforms.normalMatrix * input.normal); // Transform the normal    

class VertexShaderBuilder(ShaderBuilder):
    def __init__(self, vertex_table: VertexTable) -> None:
        super().__init__(vertex_table)
        self(vertex_shader_code)

    def build(self) -> wgpu.ShaderModule :
        logger.debug("Building vertex shader")
        self.build_return()
        super().build()
        logger.debug(f"vertex_shader_code:\n{self.shader_code}")
        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, self.shader_code
        )
        return shader_module

    def build_return(self):
        if self.vertex_table.has('tangent'):
            #self('output.tangent = normalize(uniforms.normalMatrix * input.tangent.xyz);')
            self('output.tangent = normalize(((uniforms.transformMatrix * vec4(input.tangent.xyz, 0.0))).xyz);')
            self('output.bitangent = (cross(output.normal, output.tangent) * input.tangent.w);')
        for column in self.vertex_table.columns:
            if column.name in ['pos', 'normal', 'tangent']:
                continue

            self(f'output.{column.name} = input.{column.name};')
        self('return output;')
        self('}')

    '''
    def build_return(self):
        self.write('return VertexOutput(vert_pos')
        for column in self.vertex_table.columns:
            if column.name == 'pos':
                continue
            if column.name in ['normal', 'tangent', 'bitangent']:
                self.write(f', normalize(uniforms.normalMatrix * in.{column.name})')
                continue

            self.write(f', in.{column.name}')
        self.write(');\n')
        self('}')
    '''