from crunge.engine import Renderer, App
#from crunge.engine.imgui import ImGuiView
from crunge import imgui

from ..menubar import MenubarLocation
from crunge.engine.view import View

class Page(View):
    def __init__(self, name: str, title: str):
        super().__init__()
        self.name = name
        self.title = title
        #self.fullwidth = True
        #self.fullheight = True

    @classmethod
    def produce(cls, app: App, name: str, title: str):
        page = cls(name, title).config(window=app).create()
        return page

    def reset(self):
        io = imgui.get_io()
        io.config_flags |= imgui.ConfigFlags.DOCKING_ENABLE
