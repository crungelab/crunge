import arcade
from crunge import imgui

from . import Page


class Index(Page):
    def draw(self):
        imgui.begin("Index")

        imgui.text("Welcome to the AimPlot Demo!")
        
        imgui.end()

def install(app):
    app.add_page(Index, "index", "Index")