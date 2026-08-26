from ....composition import Composition, DrawApi

from ..render_pass_3d import RenderPass3D
from .bucket_phase_3d import BucketPhase3D
from .render_item_3d import Transmissive3D


class TransmissivePhase3D(BucketPhase3D[Transmissive3D]):
    def render(self) -> None:
        composition = Composition.get_current()
        with composition.gpu() as encoder:
            self.current_renderer.easel.snap(encoder)
        with self.current_renderer.render_pass(
            RenderPass3D(self.current_renderer.easel)
        ):
            self.render_items()

    def render_items(self):
        camera = self.current_renderer.camera_3d
        # sort by depth
        self.items.sort(
            key=lambda d: camera.depth_of(d.node),
            reverse=True,
        )
        for d in self.items:
            d.callback()