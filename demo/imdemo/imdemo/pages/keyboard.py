from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class KeyboardPage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        '''
        imgui.label_text(str(imgui.is_key_down()), "is down")
        imgui.label_text(str(imgui.get_key_index()), "index")
        imgui.label_text(str(imgui.is_key_pressed), "is pressed")
        imgui.label_text(str(imgui.is_key_released), "is released")
        '''
        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(KeyboardPage, "keyboard", "Keyboard")
    app.add_channel(PageChannel(KeyboardPage, "keyboard", "Keyboard"))
