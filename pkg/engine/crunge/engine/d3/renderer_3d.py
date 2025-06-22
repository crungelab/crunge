from ..renderer import Renderer

from .camera_3d import Camera3D
from .lighting_3d import Lighting3D

from .render_pass_3d import RenderPass3D

class Renderer3D(Renderer):
    def __init__(self, viewport, camera:Camera3D=None, lighting: Lighting3D=None) -> None:
        super().__init__(viewport, camera_3d=camera, lighting_3d=lighting)
        self.render_passes = [
            RenderPass3D(viewport, first=True),
            RenderPass3D(viewport, first=False)
        ]

    def end_pass(self):
        self.camera_3d.flush_deferred(self)
        super().end_pass()
        #self.viewport.snap(self.encoder)
