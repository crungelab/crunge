from loguru import logger

from crunge.engine.imgui import ImGuiView

from ..renderer import Renderer

from .renderer_3d import Renderer3D
from .scene_3d import Scene3D
from .camera_3d import Camera3D


class View3D(ImGuiView):
    renderer: Renderer3D

    def __init__(self, scene: Scene3D) -> None:
        super().__init__()
        self.scene = scene
        self.camera: Camera3D = None

    def create_camera(self):
        self.camera = Camera3D(viewport_size=self.window.viewport.size)

    def create_renderer(self):
        self.renderer = Renderer3D(self.window.viewport, self.camera, self.scene.lighting)

    def draw(self, renderer: Renderer):
        with self.renderer:
            self.scene.draw(self.renderer)
        super().draw(self.renderer)
