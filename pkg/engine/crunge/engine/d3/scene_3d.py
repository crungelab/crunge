from ctypes import sizeof

from loguru import logger
import glm

from crunge.core import as_capsule
from crunge import wgpu

from ..light import AmbientLight

from .node_3d import Node3D
from .renderer_3d import Renderer3D
from .lighting_3d import Lighting3D

class Scene3D(Node3D):
    def __init__(self) -> None:
        super().__init__()
        self.scene = self

        self.ambient_light = AmbientLight()

        self.lighting = Lighting3D()

    def draw(self, renderer: Renderer3D):
            self.ambient_light.apply()

            super().draw(renderer)
