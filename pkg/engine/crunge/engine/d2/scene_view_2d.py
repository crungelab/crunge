from loguru import logger
import glm

from ..renderer import Renderer
from .scene_2d import Scene2D
from .view_2d import View2D

class SceneView2D(View2D):
    def __init__(self, scene: Scene2D) -> None:
        super().__init__()
        self.scene = scene

    def pre_draw(self, renderer: Renderer):
        self.scene.pre_draw(self.renderer)
        super().pre_draw(self.renderer)

    def draw(self, renderer: Renderer):
        with self.renderer:
            self.scene.draw(self.renderer)
            super().draw(self.renderer)

    def post_draw(self, renderer: Renderer):
        self.scene.post_draw(self.renderer)
        super().post_draw(self.renderer)

    def update(self, dt: float):
        self.scene.update(dt)
        super().update(dt)
