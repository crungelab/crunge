from loguru import logger

from ..node import Node

class Scene2D(Node):
    def __init__(self) -> None:
        super().__init__()
        self.scene = self
