from loguru import logger

from crunge import gltf

from .node_builder import NodeBuilder
from .builder_context import BuilderContext
from ..debug import (
    debug_mesh,
)

from crunge.engine.d3.mesh_instance_3d import MeshInstance3D

from .mesh_builder import MeshBuilder


class MeshNodeBuilder(NodeBuilder):
    def __init__(self, context: BuilderContext, tf_node: gltf.Node) -> None:
        super().__init__(context, tf_node)

    def create_node(self):
        self.node = MeshInstance3D()

    def build_node(self):
        super().build_node()
        self.node.mesh = MeshBuilder(self.context, self.tf_node.mesh).build()
