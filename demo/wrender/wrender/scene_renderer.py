from crunge import wgpu, engine

from .camera import Camera

class SceneRenderer(engine.Renderer):
    def __init__(self) -> None:
        super().__init__()
        self.pass_enc: wgpu.RenderPassEncoder = None
        self.camera: Camera = None