from crunge import imgui
from crunge.imgui import rel

from imdemo.page import Page


class FontImage(Page):
    def draw(self):
        super().draw()
        imgui.begin("Image example")
        tex_id = imgui.get_io().fonts.tex_id
        draw_list = imgui.get_window_draw_list()
        draw_list.add_image(tex_id, rel(0, 0), rel(512, 64), col=imgui.get_color_u32((0.5,0.5,1,1)))
        imgui.end()

def install(app):
    app.add_page(FontImage, "fontimage", "Font Image")
