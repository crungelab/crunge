from loguru import logger
import glm

from crunge import wgpu
import crunge.wgpu.utils as utils

from crunge.engine.imgui import ImGuiView

from ..constants import *
from crunge.engine import Renderer
from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.camera_2d import Camera2D


class DemoView(ImGuiView):
    renderer: Renderer = None

    def __init__(self, scene: Scene2D, size=glm.ivec2()) -> None:
        super().__init__(size)
        self.scene = scene

    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2), glm.vec2(self.width, self.height)
        )

    def create_renderer(self):
        self.renderer = Renderer(self.window.viewport, camera_2d=self.camera)

    def draw(self, renderer: Renderer):
        with self.renderer:
            self.scene.draw(self.renderer)

        super().draw(renderer)
