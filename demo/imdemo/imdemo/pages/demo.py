from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class DemoPage(Page):
    def _draw(self):
        imgui.show_demo_window()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(DemoPage, 'demo', 'Demo in Demo'))
