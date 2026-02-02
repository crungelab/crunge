from uuid import uuid4

from crunge import engine
from ..overlay import ImGuiOverlay


class Widget(engine.Widget):
    def __init__(self, children=None):
        super().__init__()
        if children is None:
            children = []
        self.id = uuid4()
        self.add_children(children)

    @property
    def gui(self) -> ImGuiOverlay | None:
        return ImGuiOverlay.get_current()

"""
class Widget(engine.Widget):
    def __init__(self, children=None):
        super().__init__()
        if children is None:
            children = []
        self.id = uuid4()
        self.add_children(children)
        self.gui = None

    def set_gui(self, gui: ImGuiOverlay):
        self.gui = gui
        return self
"""