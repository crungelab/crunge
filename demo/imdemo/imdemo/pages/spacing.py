from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class SpacingPage(Page):
    def _draw(self):
        imgui.begin(self.title)

        imgui.text("Some text with bullets:")
        imgui.bullet_text("Bullet A")
        imgui.bullet_text("Bullet A")

        imgui.spacing(); imgui.spacing()

        imgui.text("Another text with bullets:")
        imgui.bullet_text("Bullet A")
        imgui.bullet_text("Bullet A")

        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(SpacingPage, "spacing", "Spacing"))
