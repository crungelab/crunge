from ...viewport import Viewport
from ...renderer import Renderer
from ...renderer.task import RenderPlan
from ...renderer.task.filter_phase import FilterPhase
from ...renderer.task.composite_phase import CompositePhase

from ..camera_2d import Camera2D

from .render_pass_2d import RenderPass2D
from .task import OpaquePhase2D


class Renderer2D(Renderer):
    def __init__(
        self, viewport: Viewport, camera: Camera2D = None, clear: bool = True
    ) -> None:
        super().__init__(viewport, camera_2d=camera, clear=clear)

    def create_render_pass(self):
        clear = self.first_pass and self.clear
        return RenderPass2D(self.viewport, clear=clear)

    def create_plan(self) -> None:
        phases = [
            OpaquePhase2D(),
            FilterPhase(),
            CompositePhase(),
        ]
        self.plan = RenderPlan(phases)
