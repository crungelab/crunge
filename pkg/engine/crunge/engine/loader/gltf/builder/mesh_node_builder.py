from loguru import logger

from crunge import gltf

from .node_builder import NodeBuilder
from .builder_context import BuilderContext
from ..debug import (
    debug_mesh,
)

from crunge.engine.d3.mesh_node_3d import MeshNode3D

from .mesh_builder import MeshBuilder


class MeshNodeBuilder(NodeBuilder):
    def __init__(self, context: BuilderContext, tf_node: gltf.Node) -> None:
        super().__init__(context, tf_node)
        self.tf_mesh = self.tf_model.meshes[self.tf_node.mesh]
        self.mesh_node: MeshNode3D = None

    def create_node(self):
        self.node = self.mesh_node = MeshNode3D()

    def build_node(self):
        super().build_node()
        debug_mesh(self.tf_mesh)
        mesh_builder = MeshBuilder(self.context, self.tf_mesh)
        mesh = mesh_builder.build()
        self.mesh_node.mesh = mesh