from loguru import logger

from crunge.engine.imgui import ImGuiView

from .renderer.renderer_3d import Renderer3D
from .scene_3d import Scene3D
from .camera_3d import Camera3D


class View3D(ImGuiView):
    renderer: Renderer3D

    def __init__(self) -> None:
        super().__init__()
        self.camera: Camera3D = None

    def create_camera(self):
        self.camera = Camera3D()

    def create_renderer(self):
        self.renderer = Renderer3D(self.window.viewport, self.camera, self.scene.lighting)
