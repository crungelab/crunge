from pathlib import Path

from loguru import logger

from crunge import gltf

from . import GltfBuilder
from .builder_context import BuilderContext
from ....d3.scene_3d import Scene3D
#from .node_builder import NodeBuilder
from .poly_node_builder import PolyNodeBuilder

from ..debug import debug_node

class SceneBuilder(GltfBuilder):
    def __init__(self, context: BuilderContext, tf_scene: gltf.Scene) -> None:
        super().__init__(context)
        self.tf_scene = tf_scene
    
    def build(self) -> Scene3D:
        logger.debug(f"Building Scene: {self.tf_scene.name}")
        self.build_nodes()
        return self.scene
    
    def build_nodes(self) -> None:
        for sc_node in self.tf_scene.nodes:
            tf_node = self.tf_model.nodes[sc_node]
            self.build_node(tf_node)

    def build_node(self, tf_node) -> None:
        node = PolyNodeBuilder(self.context, tf_node).build()
        self.scene.primary_layer.attach(node)
