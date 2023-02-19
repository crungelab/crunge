from pathlib import Path

from loguru import logger
import numpy as np
import trimesh as tm

from crunge.core import as_capsule
from crunge import wgpu
import crunge.wgpu.utils as utils

from . import utils
from .builder import Builder
from .scene import Scene
from .mesh import Mesh
from .mesh_builder import MeshBuilder

class SceneBuilder(Builder):
    scene: Scene
    tm_scene: tm.Scene

    def __init__(self) -> None:
        self.scene = Scene()
    
    def load(self, path:Path):
        self.scene = scene = Scene()
        self.tm_scene = tm_scene = tm.load(str(path))
        logger.debug(tm_scene.__dict__)
        logger.debug(tm_scene.graph.__dict__)
        logger.debug(tm_scene.graph.transforms.edge_data)
        logger.debug(tm_scene.graph.transforms.node_data)
        self.create_meshes()
        return scene

    def create_meshes(self):
        tm_meshes = list(self.tm_scene.geometry.values())
        logger.debug(tm_meshes)
        for tm_mesh in tm_meshes:
            self.create_mesh(tm_mesh)

    def create_mesh(self, tm_mesh):
        mesh_builder = MeshBuilder(self.scene)
        mesh = mesh_builder.build(tm_mesh)
        self.scene.add_child(mesh)