from loguru import logger

from ..renderer.renderer_3d import Renderer3D

from ..scene.scene_3d import Scene3D
from .view_3d import View3D


class SceneView3D(View3D):
    renderer: Renderer3D

    def __init__(self, scene: Scene3D) -> None:
        super().__init__()
        self.scene = scene

    def create_renderer(self) -> None:
        self.renderer = Renderer3D(viewport=self.viewport, camera=self.camera, lighting=self.scene.lighting)

    def draw(self):
        with self.renderer.use():
            self.renderer.render(self.scene)
            super().draw()

    """
    def _draw(self):
        with self.renderer.frame():
            self.renderer.render(self.scene)

        with self.renderer.use():
            super()._draw()
    """