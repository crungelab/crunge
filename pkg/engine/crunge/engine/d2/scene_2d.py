from loguru import logger

from ..scene import Scene
from .node_2d import Node2D
from .renderer_2d import Renderer2D

class Scene2D(Scene[Node2D, Renderer2D]):
    def __init__(self) -> None:
        super().__init__()
        self.root = Node2D()
        self.root.scene = self
