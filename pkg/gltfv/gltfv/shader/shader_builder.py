from ..builder import Builder
from ..vertex_table import VertexTable


shader_code_preamble = """
struct Uniforms {
  modelViewProjectionMatrix : mat4x4<f32>,
}
@group(0) @binding(0) var<uniform> uniforms : Uniforms;

struct VertexInput {
  @location(0) pos: vec4<f32>,
  @location(1) normal: vec4<f32>,
  @location(2) uv: vec2<f32>,
}

struct VertexOutput {
  @builtin(position) vertex_pos : vec4<f32>,
  @location(0) normal: vec4<f32>,
  @location(1) uv: vec2<f32>,
}

"""

class ShaderBuilder(Builder):
    def __init__(self, vertex_table: VertexTable) -> None:
        super().__init__()
        self.vertex_table = vertex_table
        self.shader_code = shader_code_preamble
        self.indentation = 0

    def __call__(self, line=""):
        if len(line):
            self.shader_code += ' ' * self.indentation * 4
            self.shader_code += line.replace('>>', '> >')
        self.shader_code += '\n'

    def __enter__(self):
        self.indent()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dedent()

    def indent(self):
        self.indentation +=1

    def dedent(self):
        self.indentation -=1
