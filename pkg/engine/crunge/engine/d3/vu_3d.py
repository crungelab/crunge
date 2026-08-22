from typing import TYPE_CHECKING

from loguru import logger
import glm

from ..renderer import Renderer
from ..math import Bounds3
from ..vu import Vu

if TYPE_CHECKING:
    from .renderer.renderer_3d import Renderer3D

from .node_3d import Node3D


class Vu3D(Vu[Node3D]):
    def __init__(self) -> None:
        super().__init__()
        self._transform = glm.mat4(1.0)
        self.bounds = Bounds3()

    @property
    def current_renderer(self) -> "Renderer3D":
        return Renderer.get_current()

    @property
    def transform(self) -> glm.mat4:
        return self._transform

    @transform.setter
    def transform(self, value: glm.mat4):
        self._transform = value
        self.on_transform()

    def on_transform(self):
        pass

    @property
    def size(self) -> glm.vec3:
        raise NotImplementedError

    def on_node_transform_change(self, node: Node3D) -> None:
        logger.debug(f"Vu3D.on_node_transform_change: {node}")
        # self.transform = node.transform
        self.transform = node.global_transform
