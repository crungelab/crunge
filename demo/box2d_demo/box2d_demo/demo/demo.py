from pathlib import Path
import timeit

from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge import engine

from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.scheduler import Scheduler
from crunge.engine.d2.scene import Scene2D
from crunge.engine.d2.camera_2d import Camera2D

from .. import globe

from .demo_view import DemoView


class Demo(engine.App):
    view: DemoView

    def __init__(self):
        super().__init__(
            title=self.__class__.__name__,
            resizable=True,
        )
        globe.screen = self
        self.controller_stack = []
        self.avatar_stack = []

        self.resource_root = (
            Path(__file__).parent.parent.parent.parent.parent / "resources"
        )

        ResourceManager().add_path_variables(
            resources=self.resource_root,
            images=self.resource_root / "images",
        )

    @property
    def camera(self) -> Camera2D:
        return self.view.camera

    @property
    def avatar(self):
        return self.avatar_stack[-1]

    def push_controller(self, controller):
        def callback(delta_time):
            self.controller = controller
            self.controller_stack.append(controller)

        Scheduler().schedule_once(callback, 0)

    def pop_controller(self):
        def callback(delta_time):
            controller = self.controller_stack.pop()
            logger.debug(f"Popping controller: {controller}")
            self.controller = self.controller_stack[-1] if self.controller_stack else None
            #self.controller_stack[-1].reset()

        Scheduler().schedule_once(callback, 0)

    def push_avatar(self, avatar):
        if avatar is None:
            raise ValueError("Avatar cannot be None")
        self.avatar_stack.append(avatar)
        globe.avatar = avatar
        if avatar is not None:
            self.push_controller(avatar.control())

    def pop_avatar(self):
        self.avatar_stack.pop()
        avatar = self.avatar
        globe.avatar = avatar
        self.pop_controller()
        return avatar

    def reset(self):
        super().reset()
        self.create_scene()
        self.create_view()
        self.center_camera()

    def create_scene(self):
        logger.debug("Creating scene")
        self.scene = Scene2D().create()
        self.scene.make_current()

    def create_view(self):
        logger.debug("Creating view")
        self.view = DemoView(self.scene)

    def center_camera(self):
        if self.camera:
            ppu = self.camera.ppu
            view_width_units = self.viewport.width / ppu
            view_height_units = self.viewport.height / ppu
            self.camera.position = glm.vec2(view_width_units / 2, view_height_units / 2)
            logger.debug(f"Camera centered at {self.camera.position}")

    '''
    def center_camera(self):
        if self.camera:
            self.camera.position = (
                glm.vec2(self.viewport.width / 2, self.viewport.height / 2)
                * self.camera.zoom
            )
            logger.debug(f"Camera centered at {self.camera.position}")
    '''

    def on_size(self):
        super().on_size()
        self.center_camera()

    def on_key(self, event: sdl.KeyboardEvent):
        key = event.key
        down = event.down
        if key == sdl.SDLK_ESCAPE and down:
            self.quit()

    def draw_stats(self):
        # Display timings
        imgui.text(f"Update time: {self.update_time:.4f}")
        imgui.text(f"Frame time: {self.frame_time:.4f}")
