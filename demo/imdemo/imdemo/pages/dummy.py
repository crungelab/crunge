from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Dummy(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: dummy elements")

        imgui.text("Some text with bullets:")
        imgui.bullet_text("Bullet A")
        imgui.bullet_text("Bullet B")

        imgui.dummy((0, 50))
        imgui.bullet_text("Text after dummy")

        imgui.end()
        super().draw(renderer)

def install(app: App):
    app.add_channel(PageChannel(Dummy, "dummy", "Dummy"))
