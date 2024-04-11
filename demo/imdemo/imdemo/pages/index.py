from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class Index(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Index")
        imgui.text("Welcome to the imgui Demo!")
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(Index, "index", "Index")