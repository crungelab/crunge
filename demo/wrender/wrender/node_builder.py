from loguru import logger

import glm

from crunge import gltf

from .model_builder import ModelBuilder
from .builder_context import BuilderContext
from .node import Node
from .debug import debug_node

class NodeBuilder(ModelBuilder):
    def __init__(self, context: BuilderContext, tf_node: gltf.Node) -> None:
        super().__init__(context)
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
        print(f"NodeBuilder.build_node: {self.tf_node.name}")
        transform = glm.mat4(1.0)

        if len(self.tf_node.translation) == 3:
            translation = glm.vec3(self.tf_node.translation)
            self.node.translation = translation
            transform = glm.translate(transform, glm.vec3(*translation))


        if len(self.tf_node.rotation) == 4:
            tf_rotation = self.tf_node.rotation
            #rotation = glm.quat(self.tf_node.rotation)
            rotation = glm.quat(tf_rotation[3], tf_rotation[0], tf_rotation[1], tf_rotation[2])
            self.node.rotation = rotation
            #q = glm.quat(rotation[3], rotation[0], rotation[1], rotation[2])
            transform = transform * glm.mat4_cast(rotation)

        if len(self.tf_node.scale) == 3:
            scale = glm.vec3(self.tf_node.scale)
            self.node.scale = scale
            transform = glm.scale(transform, glm.vec3(*scale))

        if len(self.tf_node.matrix) == 16:
            matrix = glm.mat4(*self.tf_node.matrix)
            self.node.matrix = matrix
            transform = transform * matrix

        #self.node.transform = transform

    def build_children(self):
        for tf_child in self.tf_node.children:
            child = self.build_child(self.tf_model.nodes[tf_child])
            self.node.add_child(child)

    '''
    def build_child(self, child: gltf.Node) -> Node:
        from .poly_node_builder import PolyNodeBuilder
        builder = PolyNodeBuilder(self.context, child)
        return builder.build()
    '''

    def build_child(self, child: gltf.Node) -> Node:
        if (child.mesh >= 0) and (child.mesh < len(self.tf_model.meshes)):
            from .mesh_builder import MeshBuilder
            builder = MeshBuilder(self.context, child)
        else:
            builder = NodeBuilder(self.context, child)
        return builder.build()
