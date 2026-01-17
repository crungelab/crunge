from loguru import logger

from ..math import Bounds3
from ..scene.layer.scene_layer import SceneLayer
from .node_3d import Node3D

class SceneLayer3D(SceneLayer[Node3D]):
    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.root = Node3D()
        self.root.layer = self

    @property
    def bounds(self) -> Bounds3:
        return self.root.bounds