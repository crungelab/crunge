from ..builder import Builder
from ..builder_context import BuilderContext
from ..vertex_table import VertexTable

from .shader_out import ShaderOut

shader_code_preamble = """
struct Camera {
    modelMatrix : mat4x4<f32>,
    transformMatrix : mat4x4<f32>,
    //normalMatrix: mat3x3<f32>,
    normalMatrix: mat4x4<f32>,
    position: vec3<f32>,
}
@group(0) @binding(0) var<uniform> camera : Camera;
"""


class ShaderBuilder(Builder):
    def __init__(self, context: BuilderContext, vertex_table: VertexTable) -> None:
        super().__init__(context)
        self.vertex_table = vertex_table
        self.out = ShaderOut()
        self.out(shader_code_preamble)

    @property
    def shader_code(self):
        return self.out.text

    def build(self):
        self.build_vertex_input()
        self.build_vertex_output()
    
    def build_vertex_input(self):
        self.out('struct VertexInput {')
        self.out.indent()
        for column in self.vertex_table.columns:
            self.out(f'@location({column.location}) {column.name}: {column.input_type},')
        self.out.dedent()
        self.out('}')

    def build_vertex_output(self):
        self.out("struct VertexOutput {")
        self.out.indent()
        self.out("@builtin(position) vertex_pos : vec4<f32>,")
        for column in self.vertex_table.columns:
            self.out(f"@location({column.location}) {column.name}: {column.output_type},")
        location = self.vertex_table.columns[-1].location + 1
        self.out(f"@location({location}) frag_pos: vec3<f32>,")
        location += 1
        if self.vertex_table.has("tangent"):
            self.out(f"@location({location}) bitangent: vec3<f32>,")
        self.out.dedent()
        self.out('}')
