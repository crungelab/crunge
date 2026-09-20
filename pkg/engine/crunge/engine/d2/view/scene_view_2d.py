from loguru import logger
import glm
from crunge import sdl

from crunge.core.dispatch import DispatchResult, EVENT_HANDLED, EVENT_UNHANDLED

from ..scene.scene_2d import Scene2D
from .view_2d import View2D
from ..renderer import Renderer2D


class SceneView2D(View2D):
    renderer: Renderer2D

    def __init__(self, scene: Scene2D) -> None:
        super().__init__()
        self.scene = scene

    def _create(self):
        super()._create()
        logger.debug("Creating scene children")
        self.scene.create()

    def create_renderer(self) -> None:
        self.renderer = Renderer2D(viewport=self.viewport, camera=self.camera)

    def _enable(self) -> None:
        super()._enable()
        self.scene.enable()

    def _ready(self) -> None:
        super()._ready()
        self.scene.ready()

    def teardown(self) -> None:
        self.scene.destroy()
        super().teardown()

    def draw(self):
        with self.renderer.use():
            self.renderer.render(self.scene)
            super().draw()

    """
    def dispatch(self, event) -> DispatchResult:
        if self.scene.dispatch(event):
            return EVENT_HANDLED
        return super().dispatch(event)
    """

    def on_mouse_button(self, event: sdl.MouseButtonEvent) -> DispatchResult:
        # logger.debug(f"mouse button: button={event.button}, down={event.down}")
        point = self.camera.unproject(glm.vec2(event.x, event.y))
        return self.scene.dispatch_2d(event, point)

    """
    def on_mouse_button(self, event: sdl.MouseButtonEvent) -> DispatchResult:
        # logger.debug(f"mouse button: button={event.button}, down={event.down}")
        input_event = PointerButtonEvent(
            button=PointerButton(event.button),
            pressed=event.down,
            clicks=event.clicks,
            position=self.camera.unproject(glm.vec2(event.x, event.y)),
            screen_position=glm.vec2(event.x, event.y),
        )
        return self.scene.dispatch(input_event)
    """
