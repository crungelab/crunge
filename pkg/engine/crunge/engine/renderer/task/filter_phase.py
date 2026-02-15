from .bucket_phase import BucketPhase
from ..render_pass import RenderPass
from .render_item import FilterItem

class FilterPhase(BucketPhase[FilterItem]):
    def render(self) -> None:
        #self.renderer.viewport.snap(self.renderer.encoder)
        #with self.renderer.frame():
        self.render_items()

    def render_items(self):
        for d in self.items:
            #logger.debug(f"TransmissivePhase3D: drawing item for {d.node}")
            d.callback()

    """
    def render(self) -> None:
        self.renderer.viewport.snap(self.renderer.encoder)
        with self.renderer.render_pass(RenderPass3D(self.renderer.viewport)):
            self.renderer.camera_3d.flush_deferred()
    """

    """
    def render(self) -> None:
        with self.renderer.frame():
            self.renderer.viewport.snap(self.renderer.encoder)
            with self.renderer.render_pass(RenderPass3D(self.renderer.viewport)):
                self.renderer.camera_3d.flush_deferred()
    """
