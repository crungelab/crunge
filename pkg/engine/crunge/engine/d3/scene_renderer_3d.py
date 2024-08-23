from crunge import wgpu, engine

from .camera_3d import Camera3D

class SceneRenderer3D(engine.Renderer):
    def __init__(self) -> None:
        super().__init__()
        self.pass_enc: wgpu.RenderPassEncoder = None
        self.camera: Camera3D = None