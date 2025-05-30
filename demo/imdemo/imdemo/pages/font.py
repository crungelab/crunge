from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class FontPage(Page):
    def reset(self):
        io = imgui.get_io()
        font_path = self.window.resource_root / "DroidSans.ttf"
        # self.font = io.fonts.add_font_from_file_ttf(str(font_path), 20.0)
        self.font = io.fonts.add_font_from_file_ttf(str(font_path), 20.0)
        # self.window.gui.renderer.refresh_font_texture()
        layer = self.get_layer("ImGuiLayer")
        layer.vu.refresh_font_texture()

    def draw(self, renderer: Renderer):
        imgui.begin("Font")

        imgui.text("Text displayed using default font")
        """
        with imgui.font(self.font):
            imgui.text("Text displayed using custom font")
        """
        imgui.push_font(self.font)
        imgui.text("Text displayed using custom font")
        imgui.pop_font()

        imgui.end()
        super().draw(renderer)


def install(app: App):
    app.add_channel(PageChannel(FontPage, "font", "Font"))
