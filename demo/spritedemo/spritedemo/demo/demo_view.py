from loguru import logger
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge.engine.imgui import ImGuiView

from ..constants import *
from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.renderer_2d import Renderer2D
from crunge.engine.d2.camera_2d import Camera2D


class DemoView(ImGuiView):
    renderer: Renderer2D = None

    def __init__(self, scene: Scene2D, size=glm.ivec2()) -> None:
        super().__init__(size)
        self.scene = scene

        self.create_camera()

    def on_size(self):
        super().on_size()
        self.camera.size = self.size

    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2), glm.vec2(self.width, self.height)
        )

    def create_renderer(self):
        self.renderer = Renderer2D(self.window.viewport, self.camera)

    def draw(self, renderer: Renderer2D):
        with self.renderer:
            self.scene.draw(self.renderer)

        super().draw(renderer)
