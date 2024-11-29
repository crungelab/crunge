from crunge import imgui
from crunge.engine.imgui import ImGuiView
from crunge.engine import Renderer

from imflo.graph import Graph

class Page(ImGuiView):
    def __init__(self, name, title):
        super().__init__()
        self.name = name
        self.title = title
        self.dragged = None
        self.graph = Graph()
        self.reset()
    
    def reset(self):
        self.graph.reset()

    @classmethod
    def produce(cls, app, name, title):
        page = cls(name, title).config(window=app).create()
        return page

    def start_dnd(self, dragged):
        self.dragged = dragged

    def end_dnd(self):
        dragged = self.dragged
        self.dragged = None
        return dragged

    def update(self, delta_time):
        self.graph.update(delta_time)

    def draw(self, renderer: Renderer):
        if self.window.show_metrics:
            self.window.show_metrics = imgui.show_metrics_window(p_open=True)

        self.draw_mainmenu()
        self.draw_navbar()

        imgui.set_next_window_pos((288, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((512, 512), imgui.Cond.ONCE)

        self.graph.draw()
        
        super().draw(renderer)

    def draw_navbar(self):
        imgui.set_next_window_pos((16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, self.window.height-32-16), imgui.Cond.ONCE)
        
        imgui.begin("Examples")

        if imgui.begin_list_box(f"##{id(self)}", (-1, -1)):

            #for entry in self.window.pages.values():
            for entry in self.window.channels.values():
                #opened, selected = imgui.selectable(entry['title'], entry['name'] == self.window.page.name)
                opened, selected = imgui.selectable(entry.title, entry.name == self.window.channel.name)
                if opened:
                    #self.window.show(entry['name'])
                    self.window.show_channel(entry.name)

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

                imgui.end_menu()

            imgui.end_main_menu_bar()
