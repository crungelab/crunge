from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Child(Page):
    def _draw(self):
        imgui.begin("Example: child region")

        #imgui.begin_child("region", (150, -50), border=True)
        #imgui.begin_child("region", border=True)
        imgui.begin_child("region", (150, -50), imgui.ChildFlags.BORDERS)
        imgui.text("inside region")
        imgui.end_child()

        imgui.text("outside region")
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Child, "child", "Child"))
