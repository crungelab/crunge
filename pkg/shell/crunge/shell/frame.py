from .widget import Widget
from .view import View

class Frame(Widget):
    '''
    def __init__(self) -> None:
        super().__init__()
    '''

    def show_view(self, view: View):
        self.view = view
        self.children.clear()
        self.add_child(view)
        
    def draw(self):
        #return super().on_draw()
        if self.view is not None:
            self.view.draw()
