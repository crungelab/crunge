import time
import sys

from loguru import logger

from crunge import as_capsule
from crunge import wgpu, sdl, shell, imgui

import crunge.wgpu.utils as utils

from .scene import Scene
from .view import View
from .camera import Camera
from .controller.camera import CameraController
from .controller.camera.arcball import ArcballCameraController

class Viewer(shell.App):
    kWidth = 1024
    kHeight = 768
    
    def __init__(self):
        super().__init__(self.kWidth, self.kHeight, "WRender", resizable=True)
        self.camera: Camera = None
        self.delta_time = 0

    def create_view(self, scene: Scene):
        logger.debug("Creating view")
        view = View(scene, self.kWidth, self.kHeight).create(self)
        self.show_view(view)

    def show(self, scene: Scene):
        logger.debug("Showing scene")
        self.scene = scene
        self.create_view(scene)

        self.camera = self.view.camera
        self.controller = ArcballCameraController(self, self.camera)
        self.controller.activate()

        self.run()

    def draw(self):
        imgui.begin("Example: button")
        imgui.button("Button 1")
        imgui.button("Button 2")
        imgui.end()
        super().draw()

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.keysym.sym
        state = event.state
        if key == sdl.SDLK_ESCAPE and state == 1:
            self.quit()
