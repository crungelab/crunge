from typing import TYPE_CHECKING

from ..renderer import Renderer

if TYPE_CHECKING:
    from .camera_3d import Camera3D


class Renderer3D(Renderer):
    def __init__(self, viewport, camera:"Camera3D"=None) -> None:
        super().__init__(viewport, camera_3d=camera)

    def end(self):
        self.camera_3d.flush_deferred(self)
        super().end()