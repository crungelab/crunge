from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class Index(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Index")
        imgui.text("Welcome to the imgui Demo!")
        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(Index, "index", "Index")
    app.add_channel(PageChannel(Index, "index", "Index"))
