from loguru import logger

from ..scene import Scene
from .node_2d import Node2D

class Scene2D(Scene[Node2D]):
    def __init__(self) -> None:
        super().__init__()
        self.root = Node2D()
        self.root.scene = self
