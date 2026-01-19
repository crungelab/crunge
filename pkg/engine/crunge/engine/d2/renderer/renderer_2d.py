from ...renderer import Renderer

from ..camera_2d import Camera2D

from .render_pass_2d import RenderPass2D

class Renderer2D(Renderer):
    def __init__(self, viewport, camera:Camera2D=None) -> None:
        super().__init__(viewport, camera_2d=camera)
        self.render_passes = [
            RenderPass2D(viewport, first=True),
        ]
