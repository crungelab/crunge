from loguru import logger

from .renderer.renderer_3d import Renderer3D

from .scene_3d import Scene3D
from .view_3d import View3D


class SceneView3D(View3D):
    renderer: Renderer3D

    def __init__(self, scene: Scene3D) -> None:
        super().__init__()
        self.scene = scene

    def create_renderer(self) -> None:
        self.renderer = Renderer3D(viewport=self.window.viewport, camera=self.camera, lighting=self.scene.lighting)

    def _draw(self):
        self.renderer.render(self.scene)

        with self.renderer.use():
            super()._draw()
