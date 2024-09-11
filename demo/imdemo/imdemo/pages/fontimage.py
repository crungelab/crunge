from loguru import logger

from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer

from imdemo.page import Page

class FontImage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Font Image")
        fonts = imgui.get_io().fonts
        texture_id = fonts.tex_id
        texture_width = fonts.tex_width
        #texture_width = self.gui.vu.texture.width
        texture_height = fonts.tex_height
        #texture_height = self.gui.vu.texture.height
        draw_list = imgui.get_window_draw_list()
        pos = rel(0, 0)
        pos2 = rel(texture_width, texture_height)
        draw_list.add_image(
            texture_id, pos, pos2, col=imgui.color_convert_float4_to_u32((0.5,0.5,1,1))
        )
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(FontImage, "fontimage", "Font Image")
