import os, sys
from pathlib import Path

from loguru import logger

from crunge import imgui
from crunge import implot
from crunge import imnodes

from crunge import engine
from crunge.engine import Scheduler

from crunge import demo

from .gui import PyoGui
from .pages import Page

def trim_docstring(docstring):
    if not docstring:
        return ""
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
    return "\n".join(trimmed)

resource_root = Path(__file__).parent.parent / "resources"

class ImPyoDemo(demo.Demo):
    def __init__(self):
        super().__init__("ImPyo Demo", __package__, resource_root)
        self.gui = PyoGui()
        self.sections = {}
        self.pages = {}
        self.show_metrics = False
        self.show_style_editor = False
        self.resource_path = resource_root
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

        implot.create_context()

        imnodes.create_context()
        imnodes.push_attribute_flag(
            imnodes.AttributeFlags.ENABLE_LINK_DETACH_WITH_DRAG_CLICK
        )
        # TODO:Looks too scary to wrap.
        # io = imnodes.get_io()
        # io.link_detach_with_modifier_click.modifier = imgui.get_io().key_ctrl


    """
    @property
    def page(self) -> Page:
        return self.view

    @page.setter
    def page(self, value: Page) -> None:
        self.view = value

    def use(self, name):
        logger.debug(f"use {name}")
        import importlib.util

        spec = importlib.util.find_spec(f"impyodemo.pages.{name}")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module, install = module, module.install
        install(self)

    """

    def add_section(self, title):
        if not title in self.sections.keys():
            section = {"title": title, "pages": {}}
            self.sections[title] = section
        else:
            section = self.sections[title]
        return section

    def add_page(self, klass, section_title, title=None):
        name = klass.__name__.lower()
        if not title:
            title = klass.__name__
        section = self.add_section(section_title)
        entry = {"klass": klass, "name": name, "title": title}
        self.pages[name] = entry
        section["pages"][name] = entry

    def show(self, name):
        logger.debug(f"show {name}")

        def callback(delta_time):
            entry = self.pages[name]
            self.page = page = entry["klass"].produce(self, name, entry["title"])

        Scheduler().schedule_once(callback, 0)

    def draw_gui(self):
        if self.show_metrics:
            self.show_metrics = imgui.show_metrics_window(True)

        if self.show_style_editor:
            self.show_style_editor = imgui.begin("Style Editor", True)[1]
            imgui.show_style_editor()
            imgui.end()

        self.draw_mainmenu()
        self.draw_navbar()

        # gui.set_next_window_pos((288, 32), imgui.Cond.ONCE)
        # gui.set_next_window_pos((self.window.width - 512 - 32, 32), imgui.Cond.ONCE)
        # gui.set_next_window_size((256, 512), imgui.Cond.ONCE)
        if self.fullwidth:
            x = self.width - (512 + 256) - 32
            width = 512
        else:
            x = self.width - (512) - 32
            width = 512 / 2

        if self.fullheight:
            y = 32
            height = self.height - 32 - 16
        else:
            y = 32
            height = (self.height - 32 - 16) / 2

        # gui.set_next_window_pos((self.window.width - (512+256) - 32, 32), imgui.Cond.ONCE)
        # gui.set_next_window_size((512, self.window.height-32-16), imgui.Cond.ONCE)

        imgui.set_next_window_pos((x, y), imgui.Cond.ONCE)
        imgui.set_next_window_size((width, height), imgui.Cond.ONCE)

        self.draw_transport()
        self.gui.draw()

    def draw_navbar(self):
        imgui.set_next_window_pos((self.width - 256 - 16, 32), imgui.Cond.ONCE)
        imgui.set_next_window_size((256, self.height - 32 - 16), imgui.Cond.ONCE)

        imgui.begin("Examples")

        for section in self.sections.values():
            if imgui.tree_node(section["title"]):
                for entry in section["pages"].values():
                    opened, selected = imgui.selectable(
                        entry["title"], entry["name"] == self.page.name
                    )
                    if opened:
                        self.show(entry["name"])
                imgui.tree_pop()

        imgui.end()

    def draw_mainmenu(self):
        if imgui.begin_main_menu_bar():
            # File
            if imgui.begin_menu("File", True):
                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                if clicked_quit:
                    exit(1)

                imgui.end_menu()
            # View
            if imgui.begin_menu("View", True):
                clicked_metrics, self.show_metrics = imgui.menu_item(
                    "Metrics", "Cmd+M", self.show_metrics, True
                )
                clicked_metrics, self.show_style_editor = imgui.menu_item(
                    "Style Editor", "Cmd+S", self.show_style_editor, True
                )
                imgui.end_menu()

            imgui.end_main_menu_bar()

    def draw_transport(self):
        imgui.begin(self.page.title)

        if imgui.button("Start"):
            self.page.start()
        if imgui.button("Stop"):
            self.page.stop()

        doc = self.page.__doc__
        if doc:
            imgui.text_unformatted(trim_docstring(doc))

        imgui.end()
