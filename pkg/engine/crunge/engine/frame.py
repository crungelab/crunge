from loguru import logger

from .widget import Widget
from .view import View

class Frame(Widget):
    def __init__(self, width=0, height=0, view: View = None) -> None:
        super().__init__(width, height)
        self.view = view

    def create(self):
        logger.debug("Frame.create")
        if self.view is not None:
            self.view.create(self)
            self.show_view(self.view)
        return self

    def show_view(self, view: View):
        self.view = view
        self.children.clear()
        self.add_child(view)
        
    def draw(self):
        #return super().on_draw()
        if self.view is not None:
            self.view.draw()
