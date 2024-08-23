from .renderer import Renderer
from .base import Base


class Vu(Base):
    def __init__(self) -> None:
        super().__init__()

    def pre_draw(self, renderer: Renderer):
        pass

    def draw(self, renderer: Renderer):
        pass

    def post_draw(self, renderer: Renderer):
        pass

    def update(self, delta_time: float):
        pass