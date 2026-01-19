from loguru import logger

from .scene_3d import Scene3D
from .view_3d import View3D


class SceneView3D(View3D):
    def __init__(self, scene: Scene3D) -> None:
        super().__init__()
        self.scene = scene

    def _draw(self):
        with self.renderer.render():
            self.scene.draw()

        with self.renderer.use():
            super()._draw()
