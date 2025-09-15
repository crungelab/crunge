from loguru import logger

from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class FontImage(Page):
    def _draw(self):
        imgui.begin("Font Image")
        fonts = imgui.get_io().fonts
        texture_id = fonts.tex_ref.texture_id
        texture_width = fonts.tex_data.width
        texture_height = fonts.tex_data.height
        draw_list = imgui.get_window_draw_list()
        pos = rel(0, 0)
        pos2 = rel(texture_width, texture_height)
        draw_list.add_image(
            imgui.TextureRef(texture_id), pos, pos2, col=imgui.color_convert_float4_to_u32((0.5,0.5,1,1))
        )
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(FontImage, "fontimage", "Font Image"))
