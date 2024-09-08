from pathlib import Path

from loguru import logger

from crunge import gltf

from . import Builder
from .builder_context import BuilderContext
from ....d3.scene_3d import Scene3D
#from .node_builder import NodeBuilder
from .poly_node_builder import PolyNodeBuilder

from ..debug import debug_node

class SceneBuilder(Builder):
    def __init__(self, context: BuilderContext, tf_scene: gltf.Scene) -> None:
        super().__init__(context)
        self.tf_scene = tf_scene
    
    def build(self) -> Scene3D:
        self.build_nodes()
        return self.scene
    
    def build_nodes(self) -> None:
        for sc_node in self.tf_scene.nodes:
            node = self.tf_model.nodes[sc_node]
            self.build_node(node)

    def build_node(self, tf_node) -> None:
        logger.debug(f"tf_node: {tf_node}")
        #node_builder = NodeBuilder(self.tf_model, tf_node)
        node_builder = PolyNodeBuilder(self.context, tf_node)
        node = node_builder.build()
        self.scene.root.attach(node)
