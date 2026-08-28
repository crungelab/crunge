import contextlib

from crunge import skia
from crunge import yoga
from crunge.engine import Renderer
from crunge import demo


class Page(demo.Page):
    def __init__(self, name: str, title: str):
        super().__init__(name, title)

    def debug_layout(self, layout: yoga.Layout):
        bounds = layout.get_computed_bounds()
        left = bounds.left
        top = bounds.top
        width = bounds.width
        height = bounds.height
        print(f"Node Layout: Left={left}, Top={top}, Width={width}, Height={height}")
        for child in layout.children:
            self.debug_layout(child)
