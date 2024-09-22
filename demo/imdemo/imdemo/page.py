from crunge.engine import Renderer
from crunge.engine.imgui import ImGuiView
from crunge import imgui

#class Page(engine.View):
class Page(ImGuiView):
    def __init__(self, name, title):
        super().__init__()
        self.name = name
        self.title = title
        self.fullwidth = True
        self.fullheight = True

    def reset(self):
        pass

    @classmethod
    def produce(cls, app, name, title):
        page = cls(name, title).create(app)
        page.reset()
        return page

    def draw(self, renderer: Renderer):
        if self.window.show_metrics:
            self.window.show_metrics = imgui.show_metrics_window(True)

        if self.window.show_style_editor:
            self.window.show_style_editor = imgui.begin('Style Editor', True)[1]
            imgui.show_style_editor()
            imgui.end()

        self.draw_mainmenu()
        self.draw_navbar()

        if self.fullwidth:
            x = self.window.width - (512+256) - 32
            width = 512
        else:
            x = self.window.width - (512) - 32
            width = 512/2

        if self.fullheight:
            y = 32
            height = self.window.height-32-16
        else:
            y = 32
            height = (self.window.height-32-16)/2

        #imgui.set_next_window_pos((x, y), imgui.COND_ONCE)
        imgui.set_next_window_pos((x, y), imgui.Cond.ONCE)
        imgui.set_next_window_size((width, height), imgui.Cond.ONCE)
        
    def draw_navbar(self):
        #gui.set_next_window_pos((16, 32), imgui.COND_ONCE)
        #imgui.set_next_window_pos((self.window.width - 256 - 16, 32), imgui.COND_ONCE)
        imgui.set_next_window_pos((self.window.width - 256 - 16, 32), imgui.Cond.ONCE)
        #imgui.set_next_window_size((256, self.window.height-32-16), imgui.COND_ONCE)
        imgui.set_next_window_size((256, self.window.height-32-16), imgui.Cond.ONCE)
        
        imgui.begin("Examples")

        if imgui.begin_list_box("Examples", (-1, -1)):

            for entry in self.window.pages.values():
                opened, selected = imgui.selectable(entry['title'], entry['name'] == self.window.page.name)
                if opened:
                    self.window.show(entry['name'])

            imgui.end_list_box()
        
        imgui.end()

    def draw_mainmenu(self):
        if imgui.begin_main_menu_bar():
            # File
            if imgui.begin_menu('File', True):
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", 'Cmd+Q', False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            # View
            if imgui.begin_menu('View', True):
                clicked_metrics, self.window.show_metrics = imgui.menu_item(
                    "Metrics", 'Cmd+M', self.window.show_metrics, True
                )
                clicked_metrics, self.window.show_style_editor = imgui.menu_item(
                    "Style Editor", 'Cmd+S', self.window.show_style_editor, True
                )
                imgui.end_menu()

            imgui.end_main_menu_bar()
