from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Dummy(Page):
    def _draw(self):
        imgui.begin("Example: dummy elements")

        imgui.text("Some text with bullets:")
        imgui.bullet_text("Bullet A")
        imgui.bullet_text("Bullet B")

        imgui.dummy((0, 50))
        imgui.bullet_text("Text after dummy")

        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Dummy, "dummy", "Dummy"))
