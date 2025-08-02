from crunge import imgui
from crunge.engine import Renderer
from . import Page


class About(Page):
    def _draw(self):
        imgui.begin(self.title)

        imgui.text("Welcome to the AimPyo Demo!")
        
        imgui.end()
        super()._draw()

def install(app):
    app.add_page(About, "help")