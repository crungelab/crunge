from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Index(Page):
    def _draw(self):
        imgui.begin("Index")
        imgui.text("Welcome to the ImFlo Demo!")
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Index, "index", "Index"))
