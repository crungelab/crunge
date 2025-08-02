from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class Combo(Page):
    def reset(self):
        self.options = ["first", "second", "third"]
        self.current = 2

    def _draw(self):
        imgui.begin("Example: combo widget")

        clicked, self.current = imgui.combo(
            "combo", self.current, self.options
        )
        imgui.text(f"You chose:  {self.options[self.current]}")
        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(Combo, "combo", "Combo"))
