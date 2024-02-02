from pathlib import Path

from loguru import logger

from crunge import as_capsule
from crunge import wgpu, sdl, engine, imgui
from crunge.engine import Renderer

import crunge.wgpu.utils as utils

from ..scene_renderer import SceneRenderer
from ..scene import Scene
from .demo_view import DemoView
from ..camera import Camera

#from .controller.camera import CameraController
#from .controller.camera.arcball import ArcballCameraController

class Demo(engine.App):
    renderer: SceneRenderer
    kWidth = 1024
    kHeight = 768
    
    def __init__(self):
        super().__init__(self.kWidth, self.kHeight, self.__class__.__name__, resizable=True)
        self.camera: Camera = None
        self.delta_time = 0
        self.resource_root = Path(__file__).parent.parent.parent.parent.parent / "resources"
        self.scene = Scene()

    def create(self):
        super().create()
        self.create_view()
        return self

    def create_renderer(self):
        self.renderer = SceneRenderer()

    def create_view(self):
        logger.debug("Creating view")
        view = DemoView(self.scene, self.kWidth, self.kHeight).create(self)
        self.show_view(view)
        self.camera = self.view.camera

    '''
    def draw(self, renderer: Renderer):
        imgui.begin("Example: button")
        imgui.button("Button 1")
        imgui.button("Button 2")
        imgui.end()
        super().draw(renderer)
    '''
    
    def on_key(self, event: sdl.KeyboardEvent):
        key = event.keysym.sym
        state = event.state
        if key == sdl.SDLK_ESCAPE and state == 1:
            self.quit()
