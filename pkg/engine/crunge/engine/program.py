from .renderer import Renderer
from .base import Base
from .drawable import Drawable

class Program(Base):
    def __init__(self) -> None:
        super().__init__()

    def pre_draw(self, renderer: Renderer, drawable: Drawable):
        pass

    def draw(self, renderer: Renderer, drawable: Drawable):
        pass

    def post_draw(self, renderer: Renderer, drawable: Drawable):
        pass
