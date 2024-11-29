from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


class SelectablePage(Page):
    def reset(self):
        self.selected = [False, False]

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)
        _, self.selected[0] = imgui.selectable(
            "1. I am selectable", self.selected[0]
        )
        _, self.selected[1] = imgui.selectable(
            "2. I am selectable too", self.selected[1]
        )
        imgui.text("3. I am not selectable")
        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(SelectablePage, "selectable", "Selectable")
    app.add_channel(PageChannel(SelectablePage, "selectable", "Selectable"))
