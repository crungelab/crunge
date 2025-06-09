from loguru import logger

from crunge import gltf

from .node_builder import NodeBuilder
from .builder_context import BuilderContext
from ..debug import (
    debug_mesh,
)

from crunge.engine.d3.node_3d import Node3D
from crunge.engine.d3.mesh_vu_3d import MeshVu3D


from .mesh_builder import MeshBuilder


class MeshNodeBuilder(NodeBuilder):
    def __init__(self, context: BuilderContext, tf_node: gltf.Node) -> None:
        super().__init__(context, tf_node)

    def create_node(self):
        self.node = Node3D()

    def build_node(self):
        super().build_node()
        mesh = MeshBuilder(self.context, self.tf_node.mesh).build()

        vu = MeshVu3D(mesh)

        for primitive in mesh.primitives:
            if primitive.deferred:
                vu.deferred = True

        self.node.vu = vu
        self.node.model = mesh

    '''
    def build_node(self):
        super().build_node()
        self.node.mesh = MeshBuilder(self.context, self.tf_node.mesh).build()
        for primitive in self.node.mesh.primitives:
            if primitive.deferred:
                self.node.deferred = True
    '''