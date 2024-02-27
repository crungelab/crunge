from crunge import imgui

from imflo.page import Page

from imflodemo.nodes.sine import SineNode
from imflodemo.nodes.scope import ScopeNode

class SinePage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        SineNode(self.graph, 'Sin')
        ScopeNode(self.graph, 'Scope')
    '''
    def update(self, delta_time):
        for node in self.nodes:
            node.update(delta_time)

    def draw(self):
        for node in self.nodes:
            node.draw()

        for wire in self.wires:
            wire.draw()
    '''
def install(app):
    app.add_page(SinePage, "sine", "Sine Wave")
