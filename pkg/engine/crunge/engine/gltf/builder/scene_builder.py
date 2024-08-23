from pathlib import Path

from loguru import logger

from crunge import gltf

from . import Builder
from .builder_context import BuilderContext
from ...d3.scene_3d import Scene3D
#from .node_builder import NodeBuilder
from .poly_node_builder import PolyNodeBuilder

from ..debug import debug_node

class SceneBuilder(Builder):
    def __init__(self) -> None:
        #self.scene = Scene()
        self.tf_scene: gltf.Scene = None
    
    def build(self, scene_path:Path):
        #self.scene = scene = Scene()

        loader = gltf.TinyGLTF()
        logger.debug(f"loader: {loader}")

        #self.tf_model = tf_model = gltf.Model()
        tf_model = gltf.Model()
        logger.debug(f"tf_model_: {tf_model}")
        self.context = BuilderContext(Scene3D(), tf_model)

        res, err, warn = loader.load_ascii_from_file(tf_model, str(scene_path))

        logger.debug(f"res: {res}")

        if warn:
            logger.debug(f"warn: {warn}")

        if err:
            logger.debug(f"err: {err}")

        if not res:
            logger.debug(f"Failed to load glTF: {scene_path}")
            exit()
        else:
            logger.debug(f"Loaded glTF: {scene_path}")

        self.tf_scene = tf_scene = tf_model.scenes[tf_model.default_scene]
        logger.debug(f"tf_scene: {tf_scene}")

        self.build_nodes()

        return self.scene
    
    def build_nodes(self):
        for sc_node in self.tf_scene.nodes:
            node = self.tf_model.nodes[sc_node]
            self.build_node(node)

    def build_node(self, tf_node):
        logger.debug(f"tf_node: {tf_node}")
        #node_builder = NodeBuilder(self.tf_model, tf_node)
        node_builder = PolyNodeBuilder(self.context, tf_node)
        node = node_builder.build()
        self.scene.add_child(node)
