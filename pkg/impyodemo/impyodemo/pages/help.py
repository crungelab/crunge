from crunge import imgui
from crunge.engine import Renderer
from . import Page


class About(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        imgui.text("Welcome to the AimPyo Demo!")
        
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(About, "help")