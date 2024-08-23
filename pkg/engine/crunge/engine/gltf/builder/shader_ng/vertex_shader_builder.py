from loguru import logger
import numpy as np

from crunge import wgpu
import crunge.wgpu.utils as utils

from ..vertex_table import VertexTable
from ..builder_context import BuilderContext
from .shader_builder import ShaderBuilder


vertex_shader_code = """
@vertex
fn vs_main(input : VertexInput) -> VertexOutput {
    var output : VertexOutput;
    output.frag_pos = (camera.modelMatrix * input.pos).xyz;
    output.vertex_pos = camera.transformMatrix * input.pos;
    //output.normal = camera.normalMatrix * input.normal;
    //output.normal = input.normal;
    //output.normal = (camera.normalMatrix * vec4<f32>(input.normal, 0.0)).xyz;
    output.normal = normalize((camera.normalMatrix * vec4<f32>(input.normal, 0.0)).xyz);
"""


class VertexShaderBuilder(ShaderBuilder):
    def __init__(self, context: BuilderContext, vertex_table: VertexTable) -> None:
        super().__init__(context, vertex_table)
        self.out(vertex_shader_code)

    def build(self) -> wgpu.ShaderModule:
        logger.debug("Building vertex shader")
        self.build_return()
        super().build()
        # logger.debug(f"vertex_shader_code:\n{self.shader_code}")
        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, self.shader_code
        )
        return shader_module

    def build_return(self):
        if self.vertex_table.has("tangent"):
            #self.out("output.tangent = camera.normalMatrix * input.tangent.xyz;")
            self.out("output.tangent = (camera.normalMatrix * input.tangent).xyz;")
            #self.out("output.tangent = normalize((camera.normalMatrix * input.tangent).xyz);")
            self.out("output.bitangent = (cross(output.normal, output.tangent) * input.tangent.w);")
        for column in self.vertex_table.columns:
            if column.name in ["pos", "normal", "tangent"]:
                continue

            self.out(f"output.{column.name} = input.{column.name};")
        self.out("return output;")
        self.out("}")
