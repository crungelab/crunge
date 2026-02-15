from ...viewport import Viewport
from ...renderer import Renderer
from ...renderer.task import RenderPlan

from ..camera_3d import Camera3D
from ..lighting_3d import Lighting3D

from .render_pass_3d import RenderPass3D

from .task import OpaquePhase3D, TransmissivePhase3D


class Renderer3D(Renderer):
    def __init__(
        self, viewport: Viewport, camera: Camera3D = None, lighting: Lighting3D = None
    ) -> None:
        super().__init__(viewport, camera_3d=camera, lighting_3d=lighting)

    def create_render_pass(self):
        return RenderPass3D(self.viewport, first=True)
    
    def create_plan(self) -> None:
        phases = [
            OpaquePhase3D(),
            TransmissivePhase3D()
        ]
        self.plan = RenderPlan(phases)
