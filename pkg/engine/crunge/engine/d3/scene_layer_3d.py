from loguru import logger

from ..scene_layer import SceneLayer
from .node_3d import Node3D

class SceneLayer3D(SceneLayer[Node3D]):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.root = Node3D()
        self.root.layer = self
