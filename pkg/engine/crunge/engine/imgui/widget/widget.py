from uuid import uuid4

from crunge import engine


class Widget(engine.Widget):
    def __init__(self, children=[]):
        super().__init__()
        self.id = uuid4()
        self.add_children(children)
        self.gui = None
        self.visible = True

    def create(self, gui):
        super().create()
        self.gui = gui
        for child in self.children:
            child.create(gui)
        return self
