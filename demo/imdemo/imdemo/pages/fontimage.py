from loguru import logger

from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer

from imdemo.page import Page

class FontImage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Image example")
        tex_id = imgui.get_io().fonts.tex_id
        #logger.debug(f"tex_id: {tex_id}")

        draw_list = imgui.get_window_draw_list()
        draw_list.add_image(tex_id, rel(0, 0), rel(512, 64), col=imgui.color_convert_float4_to_u32((0.5,0.5,1,1)))
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(FontImage, "fontimage", "Font Image")
