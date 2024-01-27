from .gfx import Gfx
from .render_context import RenderContext

class Renderer:
    def __init__(self) -> None:
        self.instance = self.gfx.instance
        self.device = self.gfx.device
        self.queue = self.gfx.queue

    @property
    def gfx(self):
        return Gfx()

    def render(self, context: RenderContext):
        pass