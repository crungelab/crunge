from loguru import logger
import glm

from crunge.engine.imgui import ImGuiView

from .renderer_2d import Renderer2D

from .camera_2d import Camera2D

from .scratch_overlay import ScratchOverlay


class View2D(ImGuiView):
    def __init__(self) -> None:
        super().__init__()
        self.scratch: ScratchOverlay = None
        self.camera: Camera2D = None

    def _create(self):
        super()._create()
        self.scratch = ScratchOverlay()
        self.add_layer(self.scratch)

    def create_camera(self):
        self.camera = Camera2D(glm.vec2(self.width / 2, self.height / 2))

    def create_renderer(self):
        self.renderer = Renderer2D(self.window.viewport, camera=self.camera)
