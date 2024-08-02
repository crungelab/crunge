from loguru import logger

from crunge import wgpu
import crunge.wgpu.utils as utils

from ..vertex_table import VertexTable
from .shader_builder import ShaderBuilder

class Assignment:
    def __init__(self, name: str, value: str) -> None:
        self.name = name
        self.value = value

class VertexShaderBuilder(ShaderBuilder):
    def __init__(self, vertex_table: VertexTable) -> None:
        super().__init__(vertex_table)
        self.assignments: list[Assignment] = []

    def add_assignment(self, assignment: Assignment):
        self.assignments.append(assignment)

    def build(self) -> wgpu.ShaderModule :
        logger.debug("Building vertex shader")
        self.create_assignments()
        super().build()
        shader_code = self.generate('pbr.vert.wgsl')
        logger.debug(f"vertex_shader_code:\n{shader_code}")
        #exit()
        shader_module: wgpu.ShaderModule = utils.create_shader_module(
            self.device, shader_code
        )
        return shader_module

    def create_assignments(self):
        if self.vertex_table.has('tangent'):
            self.add_assignment(Assignment('tangent', 'normalize(camera.normalMatrix * input.tangent.xyz)'))
            self.add_assignment(Assignment('bitangent', '(cross(output.normal, output.tangent) * input.tangent.w)'))

        for column in self.vertex_table.columns:
            if column.name in ['pos', 'normal', 'tangent']:
                continue
            self.add_assignment(Assignment(f'{column.name}', f'input.{column.name}'))
