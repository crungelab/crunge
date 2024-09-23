from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class Child(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: child region")

        #imgui.begin_child("region", (150, -50), border=True)
        #imgui.begin_child("region", border=True)
        imgui.begin_child("region", (150, -50), imgui.ChildFlags.BORDERS)
        imgui.text("inside region")
        imgui.end_child()

        imgui.text("outside region")
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(Child, "child", "Child")
