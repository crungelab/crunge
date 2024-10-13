from loguru import logger

from crunge import gltf

from .node_builder import NodeBuilder
from .builder_context import BuilderContext
from ..debug import (
    debug_mesh,
)

from crunge.engine.d3.mesh_node_3d import MeshNode3D

from .primitive_builder import PrimitiveBuilder


class MeshNodeBuilder(NodeBuilder):
    def __init__(self, context: BuilderContext, tf_node: gltf.Node) -> None:
        super().__init__(context, tf_node)
        self.tf_mesh = self.tf_model.meshes[self.tf_node.mesh]
        self.mesh: MeshNode3D = None

    def create_node(self):
        self.node = self.mesh = MeshNode3D()

    def build_node(self):
        super().build_node()
        debug_mesh(self.tf_mesh)
        self.build_primitives()

    def build_primitives(self):
        for tf_primitive in self.tf_mesh.primitives:
            primitive_builder = PrimitiveBuilder(self.context, self.mesh, tf_primitive)
            primitive = primitive_builder.build()
            self.mesh.add_primitive(primitive)
