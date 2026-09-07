from pathlib import Path

from loguru import logger
import glm

from crunge import sdl
from crunge import imgui
from crunge import engine

from crunge.engine.dispatch import DispatchResult, EVENT_HANDLED
from crunge.engine.resource.resource_manager import ResourceManager
from crunge.engine.scheduler import Scheduler
from crunge.engine.d2.scene import Scene2D
from crunge.engine.d2.camera_2d import Camera2D

from .. import globe

from .demo_screen import DemoScreen
from .scrolling_demo_controller import ScrollingDemoController

class Demo(engine.App):
    controller_class = ScrollingDemoController

    display: DemoScreen

    def __init__(self):
        super().__init__(
            title=self.__class__.__name__,
            resizable=True,
        )
        globe.app = self
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
        return self.display.view.camera

    @property
    def avatar(self):
        # The only piece of state here. An avatar owns its controller chip
        # for its whole lifetime, so the controller is always just
        # avatar.controller -- a parallel controller stack only gave the two
        # a chance to disagree.
        return self.avatar_stack[-1] if self.avatar_stack else None

    def push_avatar(self, avatar):
        if avatar is None:
            raise ValueError("Avatar cannot be None")

        # Deferred: pushes almost always originate inside event dispatch or
        # an update, and mutating the stack mid-walk is the same class of
        # re-entrancy problem the transform guards exist to prevent.
        def callback(delta_time):
            logger.debug(f"Pushing avatar: {avatar}")
            self.avatar_stack.append(avatar)
            globe.avatar = avatar

        Scheduler().schedule_once(callback, 0)

    def pop_avatar(self):
        def callback(delta_time):
            if not self.avatar_stack:
                logger.warning("pop_avatar on an empty stack")
                return
            logger.debug(f"Popping avatar: {self.avatar}")
            self.avatar_stack.pop()
            globe.avatar = self.avatar

        Scheduler().schedule_once(callback, 0)

    def setup(self):
        super().setup()
        self.create_scene()
        self.create_display()
        self.center_camera()

    def create_scene(self):
        logger.debug("Creating scene")
        self.scene = Scene2D()
        self.scene.make_current()

    def create_display(self):
        logger.debug("Creating display")
        self.display = DemoScreen(self.scene)

    def center_camera(self):
        if self.camera:
            ppu = self.camera.ppu
            view_width_units = self.viewport.width / ppu
            view_height_units = self.viewport.height / ppu
            self.camera.position = glm.vec2(view_width_units / 2, view_height_units / 2)
            logger.debug(f"Camera centered at {self.camera.position}")

    def on_size(self):
        super().on_size()
        self.center_camera()

    def dispatch(self, event) -> DispatchResult:
        # The widget tree gets first refusal, then the active avatar's
        # controller. Avatars live in the scene rather than the widget tree,
        # so nothing reaches them through the normal structural walk.
        if super().dispatch(event):
            return EVENT_HANDLED
        avatar = self.avatar
        #logger.debug(f"Dispatching event to avatar: {avatar}")
        result = bool(avatar and avatar.controller and avatar.controller.dispatch(event))
        #logger.debug(f"Event dispatch result: {result}")
        return result

    def on_key(self, event: sdl.KeyboardEvent):
        if event.key == sdl.SDLK_ESCAPE and event.down:
            self.quit()
            return EVENT_HANDLED

    def draw_stats(self):
        # Display timings
        imgui.text(f"Update time: {self.update_time:.4f}")
        imgui.text(f"Frame time: {self.frame_time:.4f}")