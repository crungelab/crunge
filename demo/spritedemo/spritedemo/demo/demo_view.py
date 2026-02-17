from loguru import logger

from crunge.engine.d2.view import SceneView2D
from crunge.engine.d2.camera_2d import Camera2D

#from .demo_controller import DemoController

class DemoView(SceneView2D):
    def create_camera(self):
        self.camera = Camera2D()
        #self.controller = DemoController(self.camera)
