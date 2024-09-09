from uuid import uuid4

from crunge import engine
from ..layer import ImGuiLayer

class Widget(engine.Widget):
    def __init__(self, children=[]):
        super().__init__()
        self.id = uuid4()
        self.add_children(children)
        self.gui = None
        self.visible = True

    def set_gui(self, gui: ImGuiLayer):
        self.gui = gui
        return self

    def create(self, gui):
        self._create(gui)
        self.on_create()
        return self
    
    def _create(self, gui):
        super()._create()
        self.gui = gui
        for child in self.children:
            child.create(gui)
        return self
