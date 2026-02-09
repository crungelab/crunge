from ...viewport import Viewport
from ...renderer import SceneRenderer

from ...renderer.task.filter_phase import FilterPhase

from ..camera_2d import Camera2D
from ..scene_2d import Scene2D

from .task import RenderPlan2D, OpaquePhase2D
from .render_pass_2d import RenderPass2D


class SceneRenderer2D(SceneRenderer["SceneRenderer2D", Scene2D]):
    def __init__(
        self, scene: Scene2D, viewport: Viewport, camera: Camera2D = None
    ) -> None:
        super().__init__(scene, viewport, camera_2d=camera)

    def create_render_pass(self):
        return RenderPass2D(self.viewport, first=True)

    def create_phases(self) -> None:
        phases = [
            OpaquePhase2D(self),
            FilterPhase(self),
        ]

        self.plan = RenderPlan2D(self, phases)

    """
    def create_phases(self) -> None:
        self.phases = [
            OpaquePhase2D(self),
        ]
    """

    """
    def render(self):
        with self.render_pass():
            self.scene.draw()
    """
