from crunge.engine import Renderer, App
from crunge.engine.imgui import ImGuiView
from crunge import imgui

from ..menubar import MenubarLocation


class Page(ImGuiView):
    def __init__(self, name: str, title: str):
        super().__init__()
        self.name = name
        self.title = title
        self.fullwidth = True
        self.fullheight = True

    @classmethod
    def produce(cls, app: App, name: str, title: str):
        page = cls(name, title).config(window=app).create()
        return page

    def draw(self, renderer: Renderer):
        if self.window.show_metrics:
            self.window.show_metrics = imgui.show_metrics_window(True)

        if self.window.show_style_editor:
            self.window.show_style_editor = imgui.begin("Style Editor", True)[1]
            imgui.show_style_editor()
            imgui.end()

        if self.window.menubar_location == MenubarLocation.WINDOW:
            self.draw_mainmenu()
        self.draw_navbar()

        if self.fullwidth:
            x = self.window.width - (512 + 256) - 32
            width = 512
        else:
            x = self.window.width - (512) - 32
            width = 512 / 2

        if self.fullheight:
            y = 32
            height = self.window.height - 32 - 16
        else:
            y = 32
            height = (self.window.height - 32 - 16) / 2

        imgui.set_next_window_pos((x, y), imgui.Cond.ONCE)
        imgui.set_next_window_size((width, height), imgui.Cond.ONCE)

        super().draw(renderer)

    def draw_navbar(self):
        imgui.set_next_window_pos((self.window.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, self.window.height - 32 - 16), imgui.Cond.ONCE)

        flags = imgui.WindowFlags.MENU_BAR if self.window.menubar_location == MenubarLocation.NAVBAR else imgui.WindowFlags.NONE
        imgui.begin("Examples", flags=flags)

        if self.window.menubar_location == MenubarLocation.NAVBAR:
            if imgui.begin_menu_bar():
                self.draw_menu_bar()
                imgui.end_menu_bar()

        if imgui.begin_list_box(f"##Examples", (-1, -1)):

            for channel in self.window.channels.values():
                opened, selected = imgui.selectable(
                    channel.title, channel.name == self.window.channel.name
                )
                if opened:
                    self.window.show_channel(channel.name)

            imgui.end_list_box()

        imgui.end()

    def draw_mainmenu(self):
        if imgui.begin_main_menu_bar():
            self.draw_menu_bar()
            imgui.end_main_menu_bar()

    def draw_menu_bar(self):
        if imgui.begin_menu("File", True):
            clicked_quit, selected_quit = imgui.menu_item(
                "Quit", "Cmd+Q", False, True
            )

            if clicked_quit:
                exit(1)

            imgui.end_menu()
        # View
        if imgui.begin_menu("View", True):
            clicked_metrics, self.window.show_metrics = imgui.menu_item(
                "Metrics", "Cmd+M", self.window.show_metrics, True
            )
            clicked_metrics, self.window.show_style_editor = imgui.menu_item(
                "Style Editor", "Cmd+S", self.window.show_style_editor, True
            )
            imgui.end_menu()
