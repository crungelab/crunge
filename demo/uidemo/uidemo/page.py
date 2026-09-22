import contextlib

from crunge import skia
from crunge import yoga
from crunge.engine import Renderer
from crunge import demo
from crunge.engine.ui.ui_overlay import UiOverlay

class Page(demo.Page):
    def __init__(self, name: str, title: str):
        super().__init__(name, title)
        self._ui: UiOverlay = None

    @property
    def ui(self) -> UiOverlay:
        if self._ui is None:
            ui_overlay = UiOverlay()
            self.add_overlay(ui_overlay)
            self._ui = ui_overlay

        return self._ui

    def debug_layout(self, layout: yoga.LayoutNode):
        bounds = layout.get_computed_bounds()
        left = bounds.left
        top = bounds.top
        width = bounds.width
        height = bounds.height
        print(f"Node LayoutNode: Left={left}, Top={top}, Width={width}, Height={height}")
        for child in layout.children:
            self.debug_layout(child)
