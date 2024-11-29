from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class DemoPage(Page):
    def draw(self, renderer: Renderer):
        imgui.show_demo_window()
        super().draw(renderer)

def install(app: App):
    #app.add_page(DemoPage, 'demo', 'Demo in Demo')
    app.add_channel(PageChannel(DemoPage, 'demo', 'Demo in Demo'))
