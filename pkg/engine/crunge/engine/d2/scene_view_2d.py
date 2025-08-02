from loguru import logger
import glm

from ..renderer import Renderer
from .scene_2d import Scene2D
from .view_2d import View2D

class SceneView2D(View2D):
    def __init__(self, scene: Scene2D) -> None:
        super().__init__()
        self.scene = scene

    def _draw(self):
        with self.renderer:
            self.scene.draw()
        super()._draw()

    def update(self, dt: float):
        self.scene.update(dt)
        super().update(dt)
