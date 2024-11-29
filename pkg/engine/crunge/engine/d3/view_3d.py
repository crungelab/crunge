from loguru import logger
import glm

from crunge import wgpu

from crunge.engine.imgui import ImGuiView

from ..renderer import Renderer

from .scene_3d import Scene3D
from .camera_3d import Camera3D


class View3D(ImGuiView):
    def __init__(self, scene: Scene3D) -> None:
        super().__init__()
        self.scene = scene
        #self.camera = Camera3D(size)
        self.camera:Camera3D = None

    def create_camera(self):
        self.camera = Camera3D(size=self.size)

    def create_renderer(self):
        self.renderer = Renderer(self.window.viewport, camera_3d=self.camera)

    def draw(self, renderer: Renderer):
        with self.renderer:
            self.scene.draw(self.renderer)
            super().draw(self.renderer)
