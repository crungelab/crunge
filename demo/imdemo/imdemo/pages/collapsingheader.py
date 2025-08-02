from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class CollapsingHeader(Page):
    def reset(self):
        self.visible = True

    def _draw(self):
        imgui.begin("Example: collapsing header")
        expanded, self.visible = imgui.collapsing_header("Expand me!", self.visible)

        if expanded:
            imgui.text("Now you see me!")
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(CollapsingHeader, "collapsingheader", "Collapsing Header"))
