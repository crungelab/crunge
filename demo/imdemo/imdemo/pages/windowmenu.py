from crunge import imgui
from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class WindowMenu(Page):
    def _draw(self):
        flags = imgui.WindowFlags.MENU_BAR

        imgui.begin("Child Window - File Browser", flags=flags)

        if imgui.begin_menu_bar():
            if imgui.begin_menu('File'):
                imgui.menu_item("Quit", 'Cmd+Q', False, True)
                imgui.end_menu()

            imgui.end_menu_bar()

        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(WindowMenu, "windowmenu", "Window Menu"))
