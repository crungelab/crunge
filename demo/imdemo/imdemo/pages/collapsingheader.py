from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class CollapsingHeader(Page):
    def reset(self):
        pass

    def _draw(self):
        imgui.begin("Example: collapsing header")
        if imgui.collapsing_header("Expand me!"):
            imgui.text("Now you see me!")
        imgui.end()
        super()._draw()

class CollapsingHeaderClosable(Page):
    def reset(self):
        self.h_visible = True

    def _draw(self):
        imgui.begin("Example: collapsing header")
        expanded, self.h_visible = imgui.collapsing_header("Expand me!", self.h_visible)
        if expanded:
            imgui.text("Now you see me!")
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(CollapsingHeader, "collapsingheader", "Collapsing Header"))
    app.add_channel(PageChannel(CollapsingHeaderClosable, "collapsingheaderclosable", "Collapsing Header Closable"))
