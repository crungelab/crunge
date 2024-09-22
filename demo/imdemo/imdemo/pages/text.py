from crunge import imgui
from crunge.imgui import rel
from crunge.engine import Renderer

from imdemo.page import Page

class DrawTextPage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        draw_list = imgui.get_window_draw_list()
        color = int.from_bytes(b'\xFF\xFF\x00\xFF', 'little')
        p1 = rel(100, 60)
        draw_list.add_text(p1, color, "Hello!")
        imgui.end()
        super().draw(renderer)

class TextPage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        imgui.text("Simple text")
        imgui.end()
        super().draw(renderer)

class ColoredTextPage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        imgui.text_colored((1, 0, 0, 1), "Colored text")
        imgui.end()
        super().draw(renderer)

class UnformattedTextPage(Page):
    def reset(self):
        self.text = '''
            Really ... 
            long ... 
            text
        '''

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        imgui.text_unformatted(self.text)
        imgui.end()
        super().draw(renderer)

class LabelTextPage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        imgui.label_text("my label", "my text")
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(DrawTextPage, "drawtext", "Draw Text")
    app.add_page(TextPage, "text", "Text")
    app.add_page(ColoredTextPage, "coloredtext", "Colored Text")
    app.add_page(UnformattedTextPage, "unformattedtext", "Unformatted Text")
    app.add_page(LabelTextPage, "labeltext", "Text with Label")
