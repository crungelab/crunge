from loguru import logger
import glm

from ..renderer import Renderer
from .scene_2d import Scene2D
from .view_2d import View2D

class SceneView2D(View2D):
    def __init__(self, scene: Scene2D, size=glm.ivec2()) -> None:
        super().__init__(size)
        self.scene = scene

    def draw(self, renderer: Renderer):
        with self.renderer:
            self.scene.draw(self.renderer)
            super().draw(self.renderer)
