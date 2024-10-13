from crunge import gltf

from . import GltfBuilder
from .builder_context import BuilderContext
from ....d3.node_3d import Node3D
from ..debug import debug_node

class PolyNodeBuilder(GltfBuilder):
    def __init__(self, context: BuilderContext, tf_node: gltf.Node) -> None:
        super().__init__(context)
        self.tf_node = tf_node

    def build(self) -> Node3D:
        if (self.tf_node.mesh >= 0) and (self.tf_node.mesh < len(self.tf_model.meshes)):
            from .mesh_node_builder import MeshNodeBuilder
            builder = MeshNodeBuilder(self.context, self.tf_node)
            '''
            from .mesh_builder import MeshBuilder
            builder = MeshBuilder(self.context, self.tf_node)
            '''
        else:
            from .node_builder import NodeBuilder
            builder = NodeBuilder(self.context, self.tf_node)
        return builder.build()
