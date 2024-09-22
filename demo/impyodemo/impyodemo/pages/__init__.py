import sys
from loguru import logger

from pyo import *

from crunge import imgui
from crunge.engine.imgui import ImGuiView
from crunge.engine import Renderer

def trim_docstring(docstring):
    if not docstring:
        return ''
    # Convert tabs to spaces (following the normal Python rules)
    # and split into a list of lines:
    lines = docstring.expandtabs().splitlines()
    # Determine minimum indentation (first line doesn't count):
    indent = sys.maxsize
    for line in lines[1:]:
        stripped = line.lstrip()
        if stripped:
            indent = min(indent, len(line) - len(stripped))
    # Remove indentation (first line is special):
    trimmed = [lines[0].strip()]
    if indent < sys.maxsize:
        for line in lines[1:]:
            trimmed.append(line[indent:].rstrip())
    # Strip off trailing and leading blank lines:
    while trimmed and not trimmed[-1]:
        trimmed.pop()
    while trimmed and not trimmed[0]:
        trimmed.pop(0)
    # Return a single string:
    return '\n'.join(trimmed)

class Page(ImGuiView):
    def __init__(self, name, title):
        super().__init__()
        self.name = name
        self.title = title
        self.fullwidth = True
        self.fullheight = True
        self.server = None

    @classmethod
    def produce(cls, app, name, title):
        page = cls(name, title).create(app)
        page.reset()
        return page

    '''
    @property
    def gui(self):
        return self.window.gui
    '''
    
    @property
    def resource_path(self):
        return self.window.resource_path

    def reset(self):
        if self.server:
            self.server.shutdown()
        self.create_server()
        self.gui.clear()
        self.do_reset()

    def do_reset(self):
        pass

    def start(self):
        self.start_server()
        self.do_start()

    def do_start(self):
        pass

    def create_server(self):
        logger.debug("Creating server")
        self.server = s = Server()
        s.setMidiInputDevice(4)
        s.boot()

    def start_server(self):
        self.server.start()

    def stop(self):
        self.reset()

    def close(self):
        if self.server:
            self.server.shutdown()
        self.gui.clear()

    def draw(self, renderer: Renderer):
        if self.window.show_metrics:
            self.window.show_metrics = imgui.show_metrics_window(True)

        if self.window.show_style_editor:
            self.window.show_style_editor = imgui.begin('Style Editor', True)[1]
            imgui.show_style_editor()
            imgui.end()

        self.draw_mainmenu()
        self.draw_navbar()

        #gui.set_next_window_pos((288, 32), imgui.Cond.ONCE)
        #gui.set_next_window_pos((self.window.width - 512 - 32, 32), imgui.Cond.ONCE)
        #gui.set_next_window_size((256, 512), imgui.Cond.ONCE)
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

        #gui.set_next_window_pos((self.window.width - (512+256) - 32, 32), imgui.Cond.ONCE)
        #gui.set_next_window_size((512, self.window.height-32-16), imgui.Cond.ONCE)

        imgui.set_next_window_pos((x, y), imgui.Cond.ONCE)
        imgui.set_next_window_size((width, height), imgui.Cond.ONCE)

        self.draw_transport()
        self.window.gui.draw()
        super().draw(renderer)

    def draw_navbar(self):
        imgui.set_next_window_pos((self.window.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, self.window.height-32-16), imgui.Cond.ONCE)
        
        imgui.begin("Examples")

        for section in self.window.sections.values():
            if imgui.tree_node(section['title']):
                for entry in section['pages'].values():
                    opened, selected = imgui.selectable(entry['title'], entry['name'] == self.window.page.name)
                    if opened:
                        self.window.show(entry['name'])
                imgui.tree_pop()

        
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

    def draw_transport(self):
        imgui.begin(self.title)

        if imgui.button('Start'):
            self.start()
        if imgui.button('Stop'):
            self.stop()

        if(self.__doc__):
            imgui.text_unformatted(trim_docstring(self.__doc__))

        imgui.end()
