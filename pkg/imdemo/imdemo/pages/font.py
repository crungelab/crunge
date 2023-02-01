from pathlib import Path

from crunge import imgui

from imdemo.page import Page

RESOURCE_PATH = Path(__file__).parent.parent / 'assets'

class FontPage(Page):
    def reset(self):
        io = imgui.get_io()
        font_path = self.window.resource_path / 'DroidSans.ttf'
        self.font = io.fonts.add_font_from_file_ttf(str(font_path), 20)
        self.window.gui.renderer.refresh_font_texture()

    def draw(self):
        imgui.begin("Font")

        imgui.text("Text displayed using default font")
        '''
        with imgui.font(self.font):
            imgui.text("Text displayed using custom font")
        '''
        imgui.push_font(self.font)
        imgui.text("Text displayed using custom font")
        imgui.pop_font()

        imgui.end()

def install(app):
    app.add_page(FontPage, "font", "Font")