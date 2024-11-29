from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class WindowDraw(Page):
    def draw(self, renderer: Renderer):
        sz = 20
        draw_list = imgui.get_window_draw_list()
        #rgba_color = imgui.get_color_u32((1, 1, 1, 1))
        rgba_color = int.from_bytes(b'\xFF\xFF\xFF\xFF', 'little')
        
        for i in range(0, imgui.Col.COUNT):
            name = imgui.get_style_color_name(i)
            #color = imgui.get_color_u32(imgui.get_style_color_vec4(i))
            color = imgui.get_color_u32(i)
            p1 = rel(0, i*10)
            p2 = (p1[0] + sz, p1[1] + sz)
            draw_list.add_rect_filled(p1, p2, color)
            
            p1 = rel(20, i*10)
            draw_list.add_text(p1, rgba_color, name)
        super().draw(renderer)

def install(app: App):
    #app.add_page(WindowDraw, "windowdraw", "Window Draw")
    app.add_channel(PageChannel(WindowDraw, "windowdraw", "Window Draw"))
