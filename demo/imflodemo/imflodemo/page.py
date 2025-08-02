from crunge.engine import Renderer
from crunge import demo
from imflo.graph import Graph

class Page(demo.Page):
    def __init__(self, name: str, title: str):
        super().__init__(name, title)
        self.dragged = None
        self.graph = Graph()
    
    def reset(self):
        self.graph.reset()
    
    def start_dnd(self, dragged):
        self.dragged = dragged

    def end_dnd(self):
        dragged = self.dragged
        self.dragged = None
        return dragged

    def update(self, delta_time):
        self.graph.update(delta_time)

    def _draw(self):
        self.graph.draw()
        
        super()._draw()
