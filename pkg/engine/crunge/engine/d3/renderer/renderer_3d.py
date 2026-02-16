from ...viewport import Viewport
from ...renderer import Renderer
from ...renderer.task import RenderPlan

from ..camera_3d import Camera3D
from ..lighting_3d import Lighting3D

from .render_pass_3d import RenderPass3D

from .task import OpaquePhase3D, TransmissivePhase3D


class Renderer3D(Renderer):
    def __init__(
        self, viewport: Viewport, camera: Camera3D = None, lighting: Lighting3D = None, clear: bool = True
    ) -> None:
        super().__init__(viewport, camera_3d=camera, lighting_3d=lighting, clear=clear)

    def create_render_pass(self):
        clear = self.first_pass and self.clear
        return RenderPass3D(self.viewport, clear=clear)
    
    def create_plan(self) -> None:
        phases = [
            OpaquePhase3D(),
            TransmissivePhase3D()
        ]
        self.plan = RenderPlan(phases)
