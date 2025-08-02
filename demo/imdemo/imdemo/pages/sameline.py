from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class SameLinePage(Page):
    def _draw(self):
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
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(SameLinePage, "sameline", "Same Line"))
