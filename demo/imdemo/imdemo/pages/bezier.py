from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class BezierCubic(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Bezier Cubic")
        draw_list = imgui.get_window_draw_list()
        p1 = rel(20, 35)
        p2 = rel(90, 80)
        p3 = rel(110, 180)
        p4 = rel(145, 35)
        color = imgui.get_color_u32((1, 1, 0, 1))
        draw_list.add_bezier_cubic(p1, p2, p3, p4, color, thickness=3)
        imgui.end()
        super().draw(renderer)


class BezierQuadratic(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Bezier Quadratic")
        draw_list = imgui.get_window_draw_list()
        p1 = rel(20, 35)
        p2 = rel(90, 80)
        p3 = rel(145, 35)
        color = imgui.get_color_u32((1, 1, 0, 1))
        draw_list.add_bezier_quadratic(p1, p2, p3, color, thickness=3)
        imgui.end()
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(BezierCubic, "beziercubic", "Bezier Cubic"))
    app.add_channel(PageChannel(BezierQuadratic, "bezierquadratic", "Bezier Quadratic"))
