from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class SameLinePage(Page):
    def draw(self, renderer: Renderer):
        imgui.begin("Example: same line widgets")

        imgui.text("same_line() with defaults:")
        imgui.button("yes"); imgui.same_line()
        imgui.button("no")

        imgui.text("same_line() with fixed position:")
        imgui.button("yes"); imgui.same_line(100)
        imgui.button("no")

        imgui.text("same_line() with spacing:")
        imgui.button("yes"); imgui.same_line(0, 50)
        imgui.button("no")

        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(SameLinePage, "sameline", "Same Line")
    app.add_channel(PageChannel(SameLinePage, "sameline", "Same Line"))
