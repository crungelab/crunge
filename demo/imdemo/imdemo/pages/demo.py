from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class DemoPage(Page):
    def draw(self, renderer: Renderer):
        imgui.show_demo_window()
        super().draw(renderer)

def install(app):
    app.add_page(DemoPage, 'demo', 'Demo in Demo')
