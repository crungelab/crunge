import contextlib

from crunge import skia
from crunge import yoga
from crunge.engine import Renderer
from crunge import demo
from crunge.engine.overlay.widget_overlay import WidgetOverlay

class Page(demo.Page):
    def __init__(self, name: str, title: str):
        super().__init__(name, title)
        self._ui: WidgetOverlay = None

    @property
    def ui(self) -> WidgetOverlay:
        if self._ui is None:
            widget_overlay = WidgetOverlay()
            self.add_overlay(widget_overlay)
            self._ui = widget_overlay

        return self._ui

    def debug_layout(self, layout: yoga.Layout):
        bounds = layout.get_computed_bounds()
        left = bounds.left
        top = bounds.top
        width = bounds.width
        height = bounds.height
        print(f"Node Layout: Left={left}, Top={top}, Width={width}, Height={height}")
        for child in layout.children:
            self.debug_layout(child)
