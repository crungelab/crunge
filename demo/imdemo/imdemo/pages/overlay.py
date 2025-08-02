from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Overlay(Page):
    def _draw(self):
        imgui.begin("Poly Line Overlay")
        draw_list = imgui.get_foreground_draw_list()
        color = imgui.get_color_u32((1, 1, 0, 1))
        draw_list.add_polyline([(20, 35), (90, 35), (55, 80)], color, closed=False, thickness=3)
        draw_list.add_polyline([(110, 35), (180, 35), (145, 80)], color, closed=True, thickness=3)

        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Overlay, "overlay", "Overlay"))
