from crunge import wgpu

from .base import Base


class Renderer(Base):
    def __init__(self) -> None:
        super().__init__()
        self.texture_view: wgpu.TextureView = None
        self.depth_stencil_view: wgpu.TextureView = None
        self.msaa_view: wgpu.TextureView = None
