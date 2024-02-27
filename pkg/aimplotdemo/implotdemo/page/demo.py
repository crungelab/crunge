from crunge import imgui
from crunge import implot

from . import Page


class DemoPage(Page):
    def draw(self):
        implot.show_demo_window()

def install(app):
    app.add_page(DemoPage, 'demo', 'Demo in Demo')
