from loguru import logger
import glm

from crunge.engine.view import View

from ..renderer.renderer_2d import Renderer2D

from ..camera_2d import Camera2D


class View2D(View):
    def __init__(self) -> None:
        super().__init__()
        self.camera: Camera2D = None

    def create_camera(self) -> None:
        self.camera = Camera2D(glm.vec2(self.width / 2, self.height / 2))
        logger.debug(f"Created camera: {self.camera}")

    def create_renderer(self) -> None:
        self.renderer = Renderer2D(self.viewport, camera=self.camera)
