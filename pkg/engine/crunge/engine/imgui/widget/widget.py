from uuid import uuid4

from crunge import engine
from ..layer import ImGuiLayer

class Widget(engine.Pane):
    def __init__(self, children=[]):
        super().__init__()
        self.id = uuid4()
        self.add_children(children)
        self.gui = None
        self.visible = True

    def set_gui(self, gui: ImGuiLayer):
        self.gui = gui
        return self

    def create(self):
        super().create()
        for child in self.children:
            child.create()
        return self
