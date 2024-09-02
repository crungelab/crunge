from pathlib import Path

from loguru import logger
import glm

from crunge import sdl
from crunge import engine

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.d2.renderer_2d import Renderer2D
from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.camera_2d import Camera2D

from .demo_view import DemoView


class Demo(engine.App):
    view: DemoView
    kWidth = 1024
    kHeight = 768

    def __init__(self):
        super().__init__(
            glm.ivec2(self.kWidth, self.kHeight),
            self.__class__.__name__,
            resizable=True,
        )
        self.delta_time = 0

        self.resource_root = (
            Path(__file__).parent.parent.parent.parent.parent / "resources"
        )

        ResourceManager().add_path_variables(
            resources=self.resource_root,
            images=self.resource_root / "images",
        )

        self.scene = Scene2D()

    @property
    def camera(self) -> Camera2D:
        return self.view.camera

    def create(self):
        super().create()
        self.create_view()
        return self

    def create_view(self):
        logger.debug("Creating view")
        view = DemoView(self.scene, self.size).create(self)
        self.show_view(view)

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        state = event.state
        if key == sdl.SDLK_ESCAPE and state == 1:
            self.quit()
