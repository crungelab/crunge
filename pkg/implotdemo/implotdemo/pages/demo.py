from crunge import imgui
from crunge import implot
from crunge.engine import Renderer

from . import Page


class DemoPage(Page):
    def draw(self, renderer: Renderer):
        implot.show_demo_window()
        super().draw(renderer)

def install(app):
    app.add_page(DemoPage, 'demo', 'Demo in Demo')
