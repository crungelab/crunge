from ctypes import sizeof

from loguru import logger
import glm


from ..renderer import Renderer

from ..light import AmbientLight

from ..scene import Scene
from .node_3d import Node3D
from .lighting_3d import Lighting3D
from .light_3d import OmniLight3D

class Scene3D(Scene[Node3D]):
    def __init__(self) -> None:
        super().__init__()
        self.root = Node3D()
        self.root.scene = self
        self.lighting = Lighting3D()
        self.root.attach(OmniLight3D(position=glm.vec3(2.0, 2.0, 2.0)))

    @property
    def ambient_light(self):
        return self.lighting.ambient_light

    def draw(self, renderer: Renderer):
            self.lighting.bind(renderer.pass_enc)
            super().draw(renderer)
