from loguru import logger

import glm

from crunge import gltf

from .model_builder import ModelBuilder
from .node import Node
from .debug import debug_node

class NodeBuilder(ModelBuilder):
    def __init__(self, tf_model: gltf.Model, tf_node: gltf.Node) -> None:
        super().__init__(tf_model)
        self.tf_node = tf_node
        self.node = None

    def build(self) -> Node:
        debug_node(self.tf_model, self.tf_node)
        self.create_node()
        self.build_node()
        self.build_children()
        return self.node

    def create_node(self):
        self.node = Node()

    def build_node(self):
        translation = glm.vec3(0.0)
        if len(self.tf_node.translation) == 3:
            translation = glm.vec3(self.tf_node.translation)
            self.node.translation = translation
        rotation = glm.mat4(1.0)
        if len(self.tf_node.rotation) == 4:
            rotation = glm.mat4(glm.quat(self.tf_node.rotation))
            self.node.rotation = rotation
        scale = glm.vec3(1.0)
        if len(self.tf_node.scale) == 3:
            scale = glm.vec3(self.tf_node.scale)
            self.node.scale = scale
        if len(self.tf_node.matrix) == 16:
            self.node.matrix = glm.mat4(self.tf_node.matrix)

    def build_children(self):
        for tf_child in self.tf_node.children:
            child = self.build_child(self.tf_model.nodes[tf_child])
            self.node.add_child(child)

    def build_child(self, child: gltf.Node) -> Node:
        from .poly_node_builder import PolyNodeBuilder
        builder = PolyNodeBuilder(self.tf_model, child)
        return builder.build()
    '''
    def build_child(self, child: gltf.Node) -> Node:
        if (self.tf_node.mesh >= 0) and (self.tf_node.mesh < len(self.tf_model.meshes)):
            from .mesh_builder import MeshBuilder
            builder = MeshBuilder(self.tf_model, child)
        else:
            builder = NodeBuilder(self.tf_model, child)
        return builder.build()
    '''