from crunge import gltf

from .model_builder import ModelBuilder
from .node import Node
from .debug import debug_node

class PolyNodeBuilder(ModelBuilder):
    def __init__(self, tf_model: gltf.Model, tf_node: gltf.Node) -> None:
        super().__init__(tf_model)
        self.tf_node = tf_node

    def build(self) -> Node:
        if (self.tf_node.mesh >= 0) and (self.tf_node.mesh < len(self.tf_model.meshes)):
            from .mesh_builder import MeshBuilder
            builder = MeshBuilder(self.tf_model, self.tf_node)
        else:
            from .node_builder import NodeBuilder
            builder = NodeBuilder(self.tf_model, self.tf_node)
        return builder.build()
