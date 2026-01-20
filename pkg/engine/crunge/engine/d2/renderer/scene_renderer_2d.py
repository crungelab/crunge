from ...viewport import Viewport

from ..camera_2d import Camera2D

from .renderer_2d import Renderer2D
from ..scene_2d import Scene2D

from .phase import OpaquePhase2D


class SceneRenderer2D(Renderer2D):
    def __init__(
        self, scene: Scene2D, viewport: Viewport, camera: Camera2D = None
    ) -> None:
        super().__init__(viewport, camera=camera)
        self.scene = scene

    def create_phases(self):
        return super().create_phases()

    def create_phases(self) -> None:
        self.phases = [
            OpaquePhase2D(self),
        ]

    """
    def render(self):
        with self.render_pass():
            self.scene.draw()
    """
