from crunge import wgpu
from crunge import engine

from .camera_3d import Camera3D

class Renderer3D(engine.Renderer):
    def __init__(self) -> None:
        super().__init__()
        self.pass_enc: wgpu.RenderPassEncoder = None
        self.camera: Camera3D = None
