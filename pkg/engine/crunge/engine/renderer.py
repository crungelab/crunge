from .gfx import Gfx
from .render_context import RenderContext
from .base import Base
class Renderer(Base):
    def __init__(self) -> None:
        super().__init__()

    def pre_draw(self):
        pass

    def draw(self):
        pass

    def post_draw(self):
        pass
