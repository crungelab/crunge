from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Ngon(Page):
    def _draw(self):
        imgui.begin("Ngon")
        draw_list = imgui.get_window_draw_list()
        color = imgui.get_color_u32((1, 1, 0, 1))
        draw_list.add_ngon(rel(100, 60), 30, color, 5)
        imgui.end()
        super()._draw()

class NgonFilled(Page):
    def _draw(self):
        imgui.begin("Ngon Filled")
        draw_list = imgui.get_window_draw_list()
        color = imgui.get_color_u32((1, 1, 0, 1))
        draw_list.add_ngon_filled(rel(100, 60), 30, color, 5)
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Ngon, "ngon", "Ngon"))
    app.add_channel(PageChannel(NgonFilled, "ngonfilled", "Ngon Filled"))
