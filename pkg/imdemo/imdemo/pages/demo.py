from crunge import imgui

from imdemo.page import Page


class DemoPage(Page):
    def draw(self):
        super().draw()
        imgui.show_demo_window()

def install(app):
    app.add_page(DemoPage, 'demo', 'Demo in Demo')
