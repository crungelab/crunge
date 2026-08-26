from crunge.engine import App
from crunge import imgui

from crunge.engine.screen import Screen


class Page(Screen):
    def __init__(self, name: str, title: str):
        super().__init__()
        self.name = name
        self.title = title

    @classmethod
    def produce(cls, app: App, name: str, title: str):
        page = cls(name, title).config(window=app).create()
        return page

    def reset(self):
        super().reset()
        gui = self.gui  # initialize the GUI overlay
        io = imgui.get_io()
        io.config_flags |= imgui.ConfigFlags.DOCKING_ENABLE
