from crunge import imgui

from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel

class Index(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Index")

        imgui.text("Welcome to the ImPlot Demo!")
        
        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(Index, "index", "Index"))