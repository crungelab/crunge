from loguru import logger

from ..scene.scene_2d import Scene2D
from .view_2d import View2D
from ..renderer import Renderer2D


class SceneView2D(View2D):
    renderer: Renderer2D

    def __init__(self, scene: Scene2D) -> None:
        super().__init__()
        self.scene = scene
        if self.enabled:
            scene.enable()

    def create_renderer(self) -> None:
        self.renderer = Renderer2D(viewport=self.viewport, camera=self.camera)

    def _enable(self) -> None:
        super()._enable()
        self.scene.enable()

    def draw(self):
        with self.renderer.use():
            self.renderer.render(self.scene)
            super().draw()

    def update(self, dt: float) -> None:
        self.scene.update(dt)
        super().update(dt)
