from loguru import logger

import numpy as np

from crunge import wgpu
from crunge.wgpu import utils
from crunge import gltf

from .constants import RESERVED_BINDINGS, TEXTURE_BINDING_START
from .node_builder import NodeBuilder
from .builder_context import BuilderContext
from .node import Node
from .debug import (
    debug_mesh,
)

from .mesh import Mesh

from .primitive_builder import PrimitiveBuilder
from .primitive import Primitive

class MeshBuilder(NodeBuilder):
    def __init__(self, context: BuilderContext, tf_node: gltf.Node) -> None:
        super().__init__(context, tf_node)
        self.tf_mesh = self.tf_model.meshes[self.tf_node.mesh]
        self.mesh: Mesh = None

    def create_node(self):
        self.node = self.mesh = Mesh()

    def build_node(self):
        super().build_node()
        debug_mesh(self.tf_mesh)
        self.build_primitives()

    def build_primitives(self):
        for tf_primitive in self.tf_mesh.primitives:
            primitive_builder = PrimitiveBuilder(self.context, self.mesh, tf_primitive)
            primitive = primitive_builder.build()
            self.mesh.add_primitive(primitive)
