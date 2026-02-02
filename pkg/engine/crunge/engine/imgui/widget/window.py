from collections.abc import Callable

from crunge import imgui

from .widget import Widget

class Window(Widget):
    _parent: None
    def __init__(self, title, children: list[Widget]=None, on_close:Callable=None, flags:int=0):
        if children is None:
            children = []
        super().__init__(children=children)
        self.title = title
        self.on_close = on_close
        self.closable = True if on_close is not None else False
        self.flags = flags

    def _draw(self):
        collapsed, opened = imgui.begin(self.title, self.closable, flags=self.flags)
        super()._draw()
        imgui.end()
        if not opened and self.closable:
            self.on_close()