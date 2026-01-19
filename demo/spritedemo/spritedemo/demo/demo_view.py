from loguru import logger

from crunge.engine.d2.renderer import Renderer2D
from crunge.engine.d2.scene_view_2d import SceneView2D
from crunge.engine.d2.camera_2d import Camera2D

class DemoView(SceneView2D):
    renderer: Renderer2D = None

    def create_camera(self):
        self.camera = Camera2D()

    def create_renderer(self):
        self.renderer = Renderer2D(self.window.viewport, camera=self.camera)
