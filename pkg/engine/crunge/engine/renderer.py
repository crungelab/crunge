from crunge import wgpu

from .base import Base

from .viewport import Viewport

class Renderer(Base):
    def __init__(self, viewport: Viewport) -> None:
        super().__init__()
        self.viewport = viewport
