from crunge import imgui

from imdemo.page import Page


class WindowMenu(Page):
    def draw(self):
        flags = imgui.WINDOW_FLAGS_MENU_BAR

        imgui.begin("Child Window - File Browser", flags=flags)

        if imgui.begin_menu_bar():
            if imgui.begin_menu('File'):
                imgui.menu_item("Quit", 'Cmd+Q', False, True)
                imgui.end_menu()

            imgui.end_menu_bar()

        imgui.end()

def install(app):
    app.add_page(WindowMenu, "windowmenu", "Window Menu")
