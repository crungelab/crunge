from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class MousePage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        #imgui.text(str(imgui.is_mouse_down(0)))
        imgui.label_text(str(imgui.get_mouse_pos()), "position")
        imgui.label_text(str(imgui.is_mouse_down(0)), "left button")
        imgui.label_text(str(imgui.is_mouse_down(1)), "right button")
        imgui.label_text(str(imgui.is_mouse_down(2)), "middle button")

        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(MousePage, "mouse", "Mouse")
    app.add_channel(PageChannel(MousePage, "mouse", "Mouse"))
