from loguru import logger
import glm

from ...math import Bounds3
from ...scene import Scene

from ..node_3d import Node3D
from .layer.graph_layer_3d import GraphLayer3D
from ..lighting_3d import Lighting3D
from ..light_3d import OmniLight3D


class Scene3D(Scene[Node3D]):
    def __init__(self) -> None:
        super().__init__("Scene3D")
        self.lighting: Lighting3D = None

    @property
    def primary_layer(self) -> GraphLayer3D:
        return self.children[0] if self.children else None

    @property
    def bounds(self) -> Bounds3:
        return self.primary_layer.bounds

    @property
    def ambient_light(self):
        return self.lighting.ambient_light

    def _seat(self) -> None:
        super()._seat()
        self.lighting = self.add(Lighting3D())

    def create_children(self) -> None:
        super().create_children()
        if not self.children:
            self.create_default_layer()

    def create_default_layer(self) -> None:
        """Create and return the default primary layer for the scene."""
        layer = GraphLayer3D("primary")
        self.add_layer(layer)
        position = glm.vec3(2.0, 2.0, 2.0)
        layer.attach(
            OmniLight3D(position=position, color=glm.vec3(1.0, 1.0, 1.0), energy=1.0)
        )
