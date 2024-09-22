from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class Overlay(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Poly Line Overlay")
        draw_list = imgui.get_foreground_draw_list()
        color = int.from_bytes(b'\xFF\xFF\x00\xFF', 'little')
        draw_list.add_polyline([(20, 35), (90, 35), (55, 80)], color, closed=False, thickness=3)
        draw_list.add_polyline([(110, 35), (180, 35), (145, 80)], color, closed=True, thickness=3)

        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(Overlay, "overlay", "Overlay")
