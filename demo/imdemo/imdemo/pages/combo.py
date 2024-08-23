from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page


class Combo(Page):
    def reset(self):
        self.options = ["first", "second", "third"]
        self.current = 2

    def draw(self, renderer: Renderer):
        imgui.begin("Example: combo widget")

        clicked, self.current = imgui.combo(
            "combo", self.current, self.options
        )
        imgui.text(f"You chose:  {self.options[self.current]}")
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(Combo, "combo", "Combo")
