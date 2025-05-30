from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Line(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Line")
        draw_list = imgui.get_window_draw_list()
        color = imgui.get_color_u32((1, 1, 0, 1))
        p1 = rel(20, 35)
        p2 = rel(180, 80)
        draw_list.add_line(p1, p2, color, 3)
        p1 = rel(180, 35)
        p2 = rel(20, 80)
        draw_list.add_line(p1, p2, color, 3)
        imgui.end()
        super().draw(renderer)

class PolyLine(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Poly Line")
        draw_list = imgui.get_window_draw_list()
        color = imgui.get_color_u32((1, 1, 0, 1))
        p1 = rel(20, 35)
        p2 = rel(90, 35)
        p3 = rel(55, 80)
        draw_list.add_polyline([p1, p2, p3], color, closed=False, thickness=3)
        p1 = rel(110, 35)
        p2 = rel(180, 35)
        p3 = rel(145, 80)
        draw_list.add_polyline([p1, p2, p3],  color, closed=True, thickness=3)
        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(Line, "line", "Line"))
    app.add_channel(PageChannel(PolyLine, "polyline", "Poly Line"))
