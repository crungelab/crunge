from loguru import logger

from ..gltf_builder import GltfBuilder
from ..builder_context import BuilderContext
from ..vertex_table import VertexTable

from .....bindings import (
    BindGroupIndex,
    CameraBindGroupLayout,
    CameraBindIndex,
)


class Attribute:
    def __init__(self, name: str, type: str, location: int) -> None:
        self.name = name
        self.type = type
        self.location = location


class Vertex:
    attributes: list[Attribute]

    def __init__(self):
        self.attributes = []

    def add_attribute(self, attribute: Attribute):
        self.attributes.append(attribute)


class VertexInput(Vertex):
    pass


class VertexOutput(Vertex):
    pass


class ShaderBuilder(GltfBuilder):
    def __init__(self, context: BuilderContext, vertex_table: VertexTable) -> None:
        super().__init__(context)
        self.vertex_table = vertex_table
        self.vertex_input = VertexInput()
        self.vertex_output = VertexOutput()

    def build(self):
        self.build_vertex_input()
        self.build_vertex_output()

    def build_vertex_input(self):
        for column in self.vertex_table.columns:
            # self(f'@location({column.location}) {column.name}: {column.input_type},')
            self.vertex_input.add_attribute(
                Attribute(column.name, column.input_type, column.location)
            )

    def build_vertex_output(self):
        for column in self.vertex_table.columns:
            self.vertex_output.add_attribute(
                Attribute(column.name, column.output_type, column.location)
            )

        location = self.vertex_table.columns[-1].location + 1
        self.vertex_output.add_attribute(Attribute("frag_pos", "vec3<f32>", location))

        location += 1
        if self.vertex_table.has("tangent"):
            self.vertex_output.add_attribute(
                Attribute("bitangent", "vec3<f32>", location)
            )

    def generate(self, template_name: str):
        template = self.context.template_env.get_template(template_name)
        dict = self.__dict__.copy()
        dict.update(
            {
                "BindGroupIndex": BindGroupIndex,
                "CameraBindIndex": CameraBindIndex,
            }
        )

        return template.render(dict)
        # return template.render(self.__dict__)
