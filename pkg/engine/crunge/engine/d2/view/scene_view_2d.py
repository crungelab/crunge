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

    # -- input -------------------------------------------------------------
    #
    # Clicks and hover share one window -> world conversion, so they can't
    # disagree about what's under the pointer.

    def _world_point(self, x: float, y: float) -> glm.vec2:
        """Window coordinates -> world. Reads the camera directly, not the
        current renderer, so it's safe from refresh() outside any render
        scope."""
        return self.camera.unproject(glm.vec2(x, y))

    def hover_portal(self, x: float, y: float):
        world = self._world_point(x, y)
        hit = self.scene.widget_at(world)
        logger.debug(f"portal: ({x:.0f}, {y:.0f}) -> world {world} -> {hit}")
        return hit

    '''
    def hover_portal(self, x: float, y: float):
        return self.scene.widget_at(self._world_point(x, y))
    '''

    """
    def dispatch(self, event) -> DispatchResult:
        if self.scene.dispatch(event):
            return EVENT_HANDLED
        return super().dispatch(event)
    """

    def on_mouse_button(self, event: sdl.MouseButtonEvent) -> DispatchResult:
        # logger.debug(f"mouse button: button={event.button}, down={event.down}")
        return self.scene.dispatch_2d(event, self._world_point(event.x, event.y))

    def on_mouse_motion(self, event: sdl.MouseMotionEvent) -> DispatchResult:
        return self.scene.dispatch_2d(event, self._world_point(event.x, event.y))
