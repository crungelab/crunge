from pathlib import Path

from loguru import logger
import numpy as np
import trimesh as tm

from crunge import wgpu

from .node import Node

class Scene(Node):
    def __init__(self) -> None:
        super().__init__()
