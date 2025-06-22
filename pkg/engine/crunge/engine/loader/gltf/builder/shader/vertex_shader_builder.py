from loguru import logger

from crunge import wgpu

from ..vertex_table import VertexTable
from ..builder_context import BuilderContext
from .shader_builder import ShaderBuilder


class Assignment:
    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value


class VertexShaderBuilder(ShaderBuilder):
    def __init__(self, context: BuilderContext, vertex_table: VertexTable) -> None:
        super().__init__(context, vertex_table)
        self.assignments: list[Assignment] = []

    def add_assignment(self, assignment: Assignment):
        self.assignments.append(assignment)

    def build(self) -> wgpu.ShaderModule:
        logger.debug("Building vertex shader")
        self.create_assignments()
        super().build()
        shader_code = self.generate("vertex.wgsl")
        # logger.debug(f"vertex_shader_code:\n{shader_code}")
        shader_module: wgpu.ShaderModule = self.gfx.create_shader_module(shader_code)
        return shader_module

    def create_assignments(self):
        if self.vertex_table.has("tangent"):
            self.add_assignment(
                Assignment(
                    "tangent", "normalize(model.normalMatrix * input.tangent).xyz"
                )
            )
            self.add_assignment(
                Assignment(
                    "bitangent",
                    "(cross(output.normal, output.tangent) * input.tangent.w)",
                )
            )

        for column in self.vertex_table.columns:
            if column.name in ["position", "normal", "tangent"]:
                continue
            self.add_assignment(Assignment(f"{column.name}", f"input.{column.name}"))
