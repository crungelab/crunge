from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class CollapsingHeader(Page):
    def reset(self):
        self.visible = True

    def draw(self, renderer: Renderer):
        imgui.begin("Example: collapsing header")
        expanded, self.visible = imgui.collapsing_header("Expand me!", self.visible)

        if expanded:
            imgui.text("Now you see me!")
        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(CollapsingHeader, "collapsingheader", "Collapsing Header")
    app.add_channel(PageChannel(CollapsingHeader, "collapsingheader", "Collapsing Header"))
