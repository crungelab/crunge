from loguru import logger
import glm

from crunge.engine.imgui import ImGuiView

from ..renderer import Renderer

from .camera_2d import Camera2D

from .scratch_layer import ScratchLayer


class View2D(ImGuiView):
    def __init__(self) -> None:
        super().__init__()
        self.scratch: ScratchLayer = None
        self.camera: Camera2D = None

    def _create(self):
        super()._create()
        self.scratch = ScratchLayer().config(view=self).create()
        self.add_layer(self.scratch)

    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2),
            glm.vec2(self.width, self.height)
        )

    def create_renderer(self):
        self.renderer = Renderer(self.window.viewport, camera_2d=self.camera)
