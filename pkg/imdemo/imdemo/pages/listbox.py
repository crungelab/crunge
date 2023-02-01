from crunge import imgui

from imdemo.page import Page

OPTIONS = ["first", "second", "third"]

class ListboxPage(Page):
    def reset(self):
        self.options = OPTIONS
        self.current = 2

    def draw(self):    
        imgui.begin(self.title)

        clicked, self.current = imgui.list_box(
            "List", self.current, self.options
        )
        imgui.text("selection: ")
        imgui.same_line()
        imgui.text(self.options[self.current])
        imgui.end()

class CustomListboxPage(Page):
    def reset(self):
        self.selected = 'second'

    def draw(self):    
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

def install(app):
    app.add_page(ListboxPage, "listbox", "Listbox")
    app.add_page(CustomListboxPage, "customlistbox", "Listbox - Custom")
