from loguru import logger

from ...view import View

from ..renderer.renderer_3d import Renderer3D
from ..camera_3d import Camera3D


class View3D(View):
    renderer: Renderer3D

    def __init__(self) -> None:
        super().__init__()
        self.camera: Camera3D = None

    def create_camera(self):
        self.camera = Camera3D()

    def create_renderer(self):
        self.renderer = Renderer3D(self.viewport, self.camera, self.scene.lighting)

    @property
    def primary_camera_3d(self) -> Camera3D:
        return self.camera
