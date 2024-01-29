from typing import Protocol

from .renderer import Renderer

class Drawable(Protocol):
    def pre_draw(self, renderer: Renderer):
        pass

    def draw(self, renderer: Renderer):
        pass

    def post_draw(self, renderer: Renderer):
        pass
