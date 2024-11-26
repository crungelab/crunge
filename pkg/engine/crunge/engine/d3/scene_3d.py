from loguru import logger
import glm


from ..renderer import Renderer
from ..scene import Scene

from .node_3d import Node3D
from .scene_layer_3d import SceneLayer3D
from .lighting_3d import Lighting3D
from .light_3d import OmniLight3D

class Scene3D(Scene[Node3D]):
    def __init__(self) -> None:
        super().__init__()
        self.lighting = Lighting3D()

    '''
    def __init__(self) -> None:
        super().__init__()
        self.primary_layer = SceneLayer3D()
        self.primary_layer.scene = self
        self.lighting = Lighting3D()
        self.primary_layer.attach(OmniLight3D(position=glm.vec3(2.0, 2.0, 2.0)))
        self.add_layer(self.primary_layer)
    '''

    def create_layers(self):
        self.primary_layer = SceneLayer3D('primary')
        self.primary_layer.scene = self
        self.primary_layer.attach(OmniLight3D(position=glm.vec3(2.0, 2.0, 2.0)))
        self.add_layer(self.primary_layer)

    @property
    def ambient_light(self):
        return self.lighting.ambient_light

    def draw(self, renderer: Renderer):
            self.lighting.bind(renderer.pass_enc)
            super().draw(renderer)
