from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class Rect(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Rectangle")
        draw_list = imgui.get_window_draw_list()
        p1 = rel(20, 35)
        p2 = rel(90, 80)
        color = int.from_bytes(b'\xFF\xFF\x00\xFF', 'little')
        draw_list.add_rect(p1, p2, color, thickness=3)
        p1 = rel(110, 35)
        p2 = rel(180, 80)
        draw_list.add_rect(p1, p2, color, rounding=5, thickness=3)
        imgui.end()
        super().draw(renderer)

class RectFilled(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Rectangle Filled")
        draw_list = imgui.get_window_draw_list()
        color = int.from_bytes(b'\xFF\xFF\x00\xFF', 'little')
        p1 = rel(20, 35)
        p2 = rel(90, 80)
        draw_list.add_rect_filled(p1, p2, color)
        p1 = rel(110, 35)
        p2 = rel(180, 80)
        draw_list.add_rect_filled(p1, p2, color, 5)
        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(Rect, "rect", "Rectangle")
    app.add_channel(PageChannel(Rect, "rect", "Rectangle"))
    #app.add_page(RectFilled, "rectfilled", "Rectangle Filled")
    app.add_channel(PageChannel(RectFilled, "rectfilled", "Rectangle Filled"))
