from typing import TYPE_CHECKING

from crunge import wgpu

from ..renderer import Renderer
from ..viewport import Viewport

if TYPE_CHECKING:
    from .camera_3d import Camera3D

class Renderer3D(Renderer):
    def __init__(self, viewport: Viewport) -> None:
        super().__init__(viewport)
        self.pass_enc: wgpu.RenderPassEncoder = None
        self.camera: Camera3D = None
