from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Circle(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Circle")
        draw_list = imgui.get_window_draw_list()
        draw_list.add_circle(rel(100, 60), 30, imgui.get_color_u32((1,1,0,1)), thickness=3)
        imgui.end()
        super().draw(renderer)

class CircleFilled(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Filled")
        draw_list = imgui.get_window_draw_list()
        draw_list.add_circle_filled(rel(100, 60), 30, imgui.get_color_u32((1,1,0,1)))
        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(Circle, "circle", "Circle"))
    app.add_channel(PageChannel(CircleFilled, "circlefilled", "Filled Circle"))


