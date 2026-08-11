from crunge import imgui
from crunge.engine import App
from crunge.demo import Page, PageChannel


class Index(Page):
    def _draw(self):
        imgui.begin("Properties")
        imgui.text("Welcome to the Spine Demo!")
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Index, "index", "Index"))
