from loguru import logger
import glm

from crunge import wgpu
from crunge.wgpu import utils

from crunge.engine.imgui import ImGuiView

from .renderer_2d import Renderer2D
from .camera_2d import Camera2D

from .scratch_layer import ScratchLayer

class View2D(ImGuiView):
    def __init__(self, size=glm.ivec2()) -> None:
        super().__init__(size)
        self.scratch: ScratchLayer = None
        self.camera: Camera2D = None

    def _create(self, window):
        super()._create(window)
        self.scratch = ScratchLayer().create(self)
        self.add_layer(self.scratch)

        self.create_camera()
        self.create_renderer()

    def on_size(self):
        super().on_size()
        size = self.size
        if self.camera is not None:
            self.camera.size = glm.vec2(size)

    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2), glm.vec2(self.width, self.height)
        )

    def create_renderer(self):
        self.renderer = Renderer2D(self.window.viewport, self.camera)

    def draw(self, renderer: Renderer2D):
        with self.renderer:
            self.scene.draw(self.renderer)
            super().draw(self.renderer)

        #super().draw(renderer)
