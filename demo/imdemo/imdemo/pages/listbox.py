from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


OPTIONS = ["first", "second", "third"]

class ListboxPage(Page):
    def reset(self):
        self.options = OPTIONS
        self.current = 2

    def _draw(self):
        imgui.begin(self.title)

        clicked, self.current = imgui.list_box(
            "List", self.current, self.options
        )
        imgui.text("selection: ")
        imgui.same_line()
        imgui.text(self.options[self.current])
        imgui.end()
        super()._draw()

class CustomListboxPage(Page):
    def reset(self):
        self.selected = 'second'

    def _draw(self):
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
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(ListboxPage, "listbox", "Listbox"))
    app.add_channel(PageChannel(CustomListboxPage, "customlistbox", "Listbox - Custom"))
