from typing import TYPE_CHECKING, Type, Dict, List, Any, Callable

if TYPE_CHECKING:
    from .camera_2d import Camera2D

from crunge import wgpu, engine

#from .camera_2d import Camera2D

class SceneRenderer(engine.Renderer):
    def __init__(self) -> None:
        super().__init__()
        self.pass_enc: wgpu.RenderPassEncoder = None
        self.camera: "Camera2D" = None