from loguru import logger

from crunge.engine.d2.view import SceneView2D
from crunge.engine.d2.camera_2d import Camera2D


class DemoView(SceneView2D):
    def create_camera(self):
        logger.debug("Creating camera")
        self.camera = Camera2D()
