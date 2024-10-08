from loguru import logger

from crunge import imgui
from crunge.engine import Renderer

from . import Widget


class WidgetGroup(Widget):
    def __init__(self, children):
        super().__init__(children)
        self.drag_index = -1
        self.dragging = None

    def draw_sortable(self, renderer: Renderer, callback=lambda i, j: None):
        hovered_index = -1
        for i, child in enumerate(self.children):
            self.draw_child(renderer, child)
            if imgui.is_item_hovered(imgui.HoveredFlags.RECT_ONLY):
                hovered_index = i

        if hovered_index > -1:
            if self.dragging and imgui.is_mouse_dragging(0):
                if hovered_index != self.drag_index:
                    self.swap(self.drag_index, hovered_index)
                    callback(self.drag_index, hovered_index)
                    self.drag_index = hovered_index

            elif imgui.is_mouse_down(0):
                self.drag_index = hovered_index
                self.dragging = self.children[hovered_index]

        if not imgui.is_mouse_down(0) and self.dragging:
            self.drag_index = -1
            self.dragging = None

    def swap(self, i, j):
        self.children[i], self.children[j] = self.children[j], self.children[i]
