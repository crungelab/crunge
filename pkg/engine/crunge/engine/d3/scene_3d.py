from loguru import logger

from .node_3d import Node3D

class Scene3D(Node3D):
    def __init__(self) -> None:
        super().__init__()
        self.scene = self
