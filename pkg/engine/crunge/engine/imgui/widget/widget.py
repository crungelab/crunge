from uuid import uuid4

from crunge import engine
from ..overlay import ImGuiOverlay

class Widget(engine.Widget):
    def __init__(self, children=[]):
        super().__init__()
        self.id = uuid4()
        self.add_children(children)
        self.gui = None

    def set_gui(self, gui: ImGuiOverlay):
        self.gui = gui
        return self

    def _create(self):
        super()._create()
        for child in self.children:
            child.create()
