from loguru import logger

import glm

from crunge import gltf

from . import GltfBuilder
from .builder_context import BuilderContext
from crunge.engine.d3.node_3d import Node3D
from ..debug import debug_node

class NodeBuilder(GltfBuilder):
    def __init__(self, context: BuilderContext, tf_node: gltf.Node) -> None:
        super().__init__(context)
        self.tf_node = tf_node
        self.node = Node3D()

    def build(self) -> Node3D:
        self.build_node()
        self.build_children()
        return self.node

    def build_node(self):
        logger.debug(f"NodeBuilder.build_node: {self.tf_node.name}")

        if len(self.tf_node.translation) == 3:
            translation = glm.vec3(self.tf_node.translation)
            self.node.position = translation

        if len(self.tf_node.rotation) == 4:
            tf_rotation = self.tf_node.rotation
            rotation = glm.quat(tf_rotation[3], tf_rotation[0], tf_rotation[1], tf_rotation[2])
            self.node.orientation = rotation

        if len(self.tf_node.scale) == 3:
            scale = glm.vec3(self.tf_node.scale)
            self.node.scale = scale

        if len(self.tf_node.matrix) == 16:
            matrix = glm.mat4(*self.tf_node.matrix)
            self.node.matrix = matrix

    def build_children(self):
        for tf_child in self.tf_node.children:
            child = self.build_child(self.tf_model.nodes[tf_child])
            self.node.attach(child)

    def build_child(self, child: gltf.Node) -> Node3D:
        from .poly_node_builder import PolyNodeBuilder
        builder = PolyNodeBuilder(self.context, child)
        return builder.build()
