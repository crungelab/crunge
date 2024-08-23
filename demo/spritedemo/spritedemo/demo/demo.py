from pathlib import Path

from loguru import logger
import glm

from crunge import wgpu, sdl, engine, imgui

from ..scene_renderer import SceneRenderer
from ..scene import Scene
from .demo_view import DemoView
from ..camera_2d import Camera2D


class Demo(engine.App):
    view: DemoView
    kWidth = 1024
    kHeight = 768

    def __init__(self):
        super().__init__(
            glm.ivec2(self.kWidth, self.kHeight), self.__class__.__name__, resizable=True
        )
        self.delta_time = 0
        self.resource_root = (
            Path(__file__).parent.parent.parent.parent.parent / "resources"
        )
        self.scene = Scene()

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
