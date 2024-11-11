from loguru import logger
import glm

from crunge.engine.imgui import ImGuiView

from ..math import Size2i
from ..renderer import Renderer

from .camera_2d import Camera2D

from .scratch_layer import ScratchLayer


class View2D(ImGuiView):
    def __init__(self, size=Size2i()) -> None:
        super().__init__(size)
        self.scratch: ScratchLayer = None
        self.camera: Camera2D = None

    #def _create(self, window):
    def _create(self):
        #super()._create(window)
        super()._create()
        #self.scratch = ScratchLayer().create(self)
        self.scratch = ScratchLayer().config(view=self).create()
        self.add_layer(self.scratch)

    def create_camera(self):
        self.camera = Camera2D(
            glm.vec2(self.width / 2, self.height / 2),
            glm.vec2(self.width, self.height)
        )

    def create_renderer(self):
        self.renderer = Renderer(self.window.viewport, camera_2d=self.camera)

    '''
    def draw(self, renderer: Renderer):
        with self.renderer:
            self.scene.draw(self.renderer)
            super().draw(self.renderer)
    '''