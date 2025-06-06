from pathlib import Path

from loguru import logger
import glm

from crunge import sdl
from crunge import engine

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.d2.scene_2d import Scene2D
from crunge.engine.d2.camera_2d import Camera2D

from .demo_view import DemoView


class Demo(engine.App):
    view: DemoView

    def __init__(self):
        super().__init__(
            title=self.__class__.__name__,
            resizable=True,
        )

        self.resource_root = (
            Path(__file__).parent.parent.parent.parent.parent / "resources"
        )

        ResourceManager().add_path_variables(
            resources=self.resource_root,
            images=self.resource_root / "images",
        )

        self.scene = Scene2D().create()

    @property
    def camera(self) -> Camera2D:
        return self.view.camera

    def _create(self):
        super()._create()
        self.create_view()

    def create_view(self):
        logger.debug("Creating view")
        self.view = DemoView(self.scene).config(window=self).create()

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        down = event.down
        if key == sdl.SDLK_ESCAPE and down:
            self.quit()
