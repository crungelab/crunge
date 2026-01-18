from loguru import logger
import glm

from ..math import Bounds3
from ..scene import Scene

from .node_3d import Node3D
from .graph_layer_3d import GraphLayer3D
from .lighting_3d import Lighting3D
from .light_3d import OmniLight3D


class Scene3D(Scene[Node3D]):
    def __init__(self) -> None:
        super().__init__()
        self.lighting = Lighting3D()

    @property
    def bounds(self) -> Bounds3:
        return self.primary_layer.bounds

    @property
    def primary_layer(self) -> GraphLayer3D:
        if not self.layers:
            #raise ValueError("No layers in the scene.")
            self.create_default_layer()
        return self.layers[0]
    
    def create_default_layer(self) -> None:
        """Create and return the default primary layer for the scene."""
        layer = GraphLayer3D('primary')
        self.add_layer(layer)
        position=glm.vec3(2.0, 2.0, 2.0)
        layer.attach(OmniLight3D(position=position, color=glm.vec3(1.0, 1.0, 1.0), energy=1.0))


    '''
    def create_layers(self):
        self.primary_layer = SceneLayer3D('primary')
        self.primary_layer.scene = self
        position=glm.vec3(2.0, 2.0, 2.0)
        self.primary_layer.attach(OmniLight3D(position=position, color=glm.vec3(1.0, 1.0, 1.0), energy=1.0))
        self.add_layer(self.primary_layer)
    '''

    @property
    def ambient_light(self):
        return self.lighting.ambient_light

    def _draw(self):
            #self.lighting.bind(renderer.pass_enc)
            super()._draw()
