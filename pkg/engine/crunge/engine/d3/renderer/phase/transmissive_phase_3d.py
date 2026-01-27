from .item_phase_3d import ItemPhase3D
from ..render_pass_3d import RenderPass3D
from .phase_item_3d import Transmissive3D

class TransmissivePhase3D(ItemPhase3D[Transmissive3D]):
    def render(self) -> None:
        with self.renderer.frame():
            self.renderer.viewport.snap(self.renderer.encoder)
            with self.renderer.render_pass(RenderPass3D(self.renderer.viewport)):
                self.renderer.camera_3d.flush_deferred()

    '''
    def render(self) -> None:
        with self.renderer.render_pass(RenderPass3D(self.renderer.viewport)):
            self.renderer.camera_3d.flush_deferred()
    '''