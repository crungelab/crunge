import contextlib

from crunge import skia
from crunge.engine import Renderer
from crunge import demo


class Page(demo.Page):
    def __init__(self, name: str, title: str):
        super().__init__(name, title)
