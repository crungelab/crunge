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
        self.gui = None

    def set_gui(self, gui: ImGuiOverlay):
        self.gui = gui
        return self

    #TODO: remove: this is handled in Node.on_added
    """
    def _enable(self):
        super()._enable()
        for child in self.children:
            child.enable()
    """

    """
    def _create(self):
        super()._create()
        for child in self.children:
            child.create()
    """