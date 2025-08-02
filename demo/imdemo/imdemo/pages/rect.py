from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Rect(Page):
    def _draw(self):
        imgui.begin("Rectangle")
        draw_list = imgui.get_window_draw_list()
        p1 = rel(20, 35)
        p2 = rel(90, 80)
        color = imgui.get_color_u32((1, 1, 0, 1))
        draw_list.add_rect(p1, p2, color, thickness=3)
        p1 = rel(110, 35)
        p2 = rel(180, 80)
        draw_list.add_rect(p1, p2, color, rounding=5, thickness=3)
        imgui.end()
        super()._draw()

class RectFilled(Page):
    def _draw(self):
        imgui.begin("Rectangle Filled")
        draw_list = imgui.get_window_draw_list()
        color = imgui.get_color_u32((1, 1, 0, 1))
        p1 = rel(20, 35)
        p2 = rel(90, 80)
        draw_list.add_rect_filled(p1, p2, color)
        p1 = rel(110, 35)
        p2 = rel(180, 80)
        draw_list.add_rect_filled(p1, p2, color, 5)
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Rect, "rect", "Rectangle"))
    app.add_channel(PageChannel(RectFilled, "rectfilled", "Rectangle Filled"))
