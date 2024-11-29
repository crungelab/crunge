from loguru import logger
import glm

from crunge.engine import Renderer
from crunge.engine.d2.scene_view_2d import SceneView2D
from crunge.engine.d2.camera_2d import Camera2D

class DemoView(SceneView2D):
    renderer: Renderer = None

    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2), glm.vec2(self.width, self.height)
        )

    def create_renderer(self):
        self.renderer = Renderer(self.window.viewport, camera_2d=self.camera)
