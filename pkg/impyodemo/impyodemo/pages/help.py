import arcade
from crunge import imgui

from . import Page


class About(Page):
    def draw(self):
        imgui.begin(self.title)

        imgui.text("Welcome to the AimPyo Demo!")
        
        imgui.end()

def install(app):
    app.add_page(About, "help")