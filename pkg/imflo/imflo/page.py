import arcade
from crunge import imgui, imnodes

#from imflo.wire import Wire
from imflo.graph import Graph

class Page(arcade.View):
    def __init__(self, window, name, title):
        super().__init__(window)
        self.name = name
        self.title = title
        self.dragged = None
        self.graph = Graph()
    
    def reset(self):
        self.graph.reset()

    @classmethod
    def create(self, app, name, title):
        page = self(app, name, title)
        page.reset()
        return page

    def start_dnd(self, dragged):
        self.dragged = dragged

    def end_dnd(self):
        dragged = self.dragged
        self.dragged = None
        return dragged

    def update(self, delta_time):
        self.graph.update(delta_time)

    def on_draw(self):
      
        arcade.start_render()

        imgui.new_frame()
        
        if self.window.show_metrics:
            self.window.show_metrics = imgui.show_metrics_window(p_open=True)

        self.draw_mainmenu()
        self.draw_navbar()

        imgui.set_next_window_pos((288, 32), imgui.COND_ONCE)
        imgui.set_next_window_size((512, 512), imgui.COND_ONCE)

        self.draw()
        
        imgui.end_frame()

    def draw_navbar(self):
        imgui.set_next_window_pos((16, 32), imgui.COND_ONCE)
        imgui.set_next_window_size((256, self.window.height-32-16), imgui.COND_ONCE)
        
        imgui.begin("Examples")

        titles = [page['title'] for page in self.window.pages.values()]
        names = [page['name'] for page in self.window.pages.values()]

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

                imgui.end_menu()

            imgui.end_main_menu_bar()

    def draw(self):
        self.graph.draw()
