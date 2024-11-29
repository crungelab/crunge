from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class SeparatorPage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        imgui.text("Some text with bullets")
        imgui.bullet_text("Bullet A")
        imgui.bullet_text("Bullet A")

        imgui.separator()

        imgui.text("Another text with bullets")
        imgui.bullet_text("Bullet A")
        imgui.bullet_text("Bullet A")

        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(SeparatorPage, "separator", "Separator")
    app.add_channel(PageChannel(SeparatorPage, "separator", "Separator"))
