from .render_phase_3d import RenderPhase3D
from ..render_pass_3d import RenderPass3D


class TransparencyPhase3D(RenderPhase3D):
    def render(self) -> None:
        with self.renderer.render_pass(RenderPass3D(self.renderer.viewport)):
            self.renderer.camera_3d.flush_deferred()
