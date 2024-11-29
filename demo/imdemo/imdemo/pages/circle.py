from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class Circle(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Circle")
        draw_list = imgui.get_window_draw_list()
        #draw_list.add_circle(rel(100, 60), 30, imgui.get_color_u32((1,1,0,1)), thickness=3)
        color = int.from_bytes(b'\xFF\xFF\x00\xFF', 'little')
        draw_list.add_circle(rel(100, 60), 30, color, thickness=3)
        imgui.end()
        super().draw(renderer)

class CircleFilled(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Filled")
        draw_list = imgui.get_window_draw_list()
        #draw_list.add_circle_filled(rel(100, 60), 30, imgui.get_color_u32((1,1,0,1)))
        color = int.from_bytes(b'\xFF\xFF\x00\xFF', 'little')
        draw_list.add_circle_filled(rel(100, 60), 30, color)
        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(Circle, "circle", "Circle")
    app.add_channel(PageChannel(Circle, "circle", "Circle"))
    #app.add_page(CircleFilled, "circlefilled", "Filled Circle")
    app.add_channel(PageChannel(CircleFilled, "circlefilled", "Filled Circle"))


