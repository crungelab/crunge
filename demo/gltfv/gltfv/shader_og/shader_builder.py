from ..builder import Builder
from ..vertex_table import VertexTable


shader_code_preamble = """
struct Camera {
    modelMatrix : mat4x4<f32>,
    transformMatrix : mat4x4<f32>,
    normalMatrix: mat3x3<f32>,
    position: vec3<f32>,
}
@group(0) @binding(0) var<uniform> camera : Camera;
"""


class ShaderBuilder(Builder):
    def __init__(self, vertex_table: VertexTable) -> None:
        super().__init__()
        self.vertex_table = vertex_table
        self.shader_code = shader_code_preamble
        self.indentation = 0

    def build(self):
        self.build_vertex_input()
        self.build_vertex_output()
    
    def build_vertex_input(self):
        self('struct VertexInput {')
        self.indent()
        for column in self.vertex_table.columns:
            self(f'@location({column.location}) {column.name}: {column.input_type},')
        self.dedent()
        self('}')

    def build_vertex_output(self):
        self('struct VertexOutput {')
        self.indent()
        self('@builtin(position) vertex_pos : vec4<f32>,')
        for column in self.vertex_table.columns:
            self(f'@location({column.location}) {column.name}: {column.output_type},')
        location = self.vertex_table.columns[-1].location + 1
        self(f'@location({location}) frag_pos: vec3<f32>,')
        location += 1
        if self.vertex_table.has('tangent'):
            self(f'@location({location}) bitangent: vec3<f32>,')
        self.dedent()
        self('}')

    def __call__(self, line=""):
        if len(line):
            self.shader_code += " " * self.indentation * 4
            self.shader_code += line.replace(">>", "> >")
        self.shader_code += "\n"

    def __enter__(self):
        self.indent()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dedent()

    def indent(self):
        self.indentation += 1

    def dedent(self):
        self.indentation -= 1

    def write(self, text: str):
        self.shader_code += text

    def write_indented(self, text: str):
        self.write(" " * self.indentation * 4)
        self.write(text)
