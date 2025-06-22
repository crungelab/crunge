from loguru import logger
import glm

from crunge.engine.d2.renderer_2d import Renderer2D
from crunge.engine.d2.scene_view_2d import SceneView2D
from crunge.engine.d2.camera_2d import Camera2D

class DemoView(SceneView2D):
    renderer: Renderer2D = None

    def create_camera(self):
        self.camera = Camera2D()

    def create_renderer(self):
        self.renderer = Renderer2D(self.window.viewport, camera=self.camera)
    '''
    def on_layout(self):
        super().on_layout()
        self.camera.position = glm.vec2(self.width / 2, self.height / 2)
    '''
