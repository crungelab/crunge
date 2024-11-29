from crunge import imgui
from crunge.engine import Renderer

from ..app import App
from ..page import Page, PageChannel


OPTIONS = ["first", "second", "third"]

class ListboxPage(Page):
    def reset(self):
        self.options = OPTIONS
        self.current = 2

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        clicked, self.current = imgui.list_box(
            "List", self.current, self.options
        )
        imgui.text("selection: ")
        imgui.same_line()
        imgui.text(self.options[self.current])
        imgui.end()
        super().draw(renderer)

class CustomListboxPage(Page):
    def reset(self):
        self.selected = 'second'

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        if imgui.begin_list_box("Custom List", (200, 100)):
            for option in OPTIONS:
                clicked, selected = imgui.selectable(option, option == self.selected)
                if clicked:
                    self.selected = option

            imgui.end_list_box()

        imgui.text("selection: ")
        imgui.same_line()
        imgui.text(self.selected)

        imgui.end()
        super().draw(renderer)

def install(app: App):
    #app.add_page(ListboxPage, "listbox", "Listbox")
    app.add_channel(PageChannel(ListboxPage, "listbox", "Listbox"))
    #app.add_page(CustomListboxPage, "customlistbox", "Listbox - Custom")
    app.add_channel(PageChannel(CustomListboxPage, "customlistbox", "Listbox - Custom"))
