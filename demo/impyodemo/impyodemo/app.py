import os, sys
from pathlib import Path

from loguru import logger

from crunge import imgui
from crunge import implot
from crunge import imnodes

from crunge import engine
from crunge.engine import Scheduler

from .gui import PyoGui
from .pages import Page


class App(engine.App):
    def __init__(self):
        super().__init__(title="ImPyo Demo", resizable=True)
        self.gui = PyoGui()
        self.sections = {}
        self.pages = {}
        self.show_metrics = False
        self.show_style_editor = False
        self.resource_path = Path(__file__).parent.parent / "resources"
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
    def add_page(self, klass, name, title):
        self.pages[name] = { 'klass': klass, 'name': name, 'title': title }
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
            # self.show_view(page)

        Scheduler().schedule_once(callback, 0)
