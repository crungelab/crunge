from loguru import logger

from ..scene_layer import SceneLayer
from .node_2d import Node2D

class SceneLayer2D(SceneLayer[Node2D]):
    def __init__(self) -> None:
        super().__init__()
        self.root = Node2D()
        self.root.layer = self
