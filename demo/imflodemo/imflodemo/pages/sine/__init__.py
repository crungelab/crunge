from imflodemo.nodes.sine import SineNode
from imflodemo.nodes.scope import ScopeNode

from ...app import App
from ...page import Page, PageChannel


class SinePage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        SineNode(self.graph, "Sin")
        ScopeNode(self.graph, "Scope")


def install(app: App):
    #app.add_page(SinePage, "sine", "Sine Wave")
    #app.add_channel(ClassChannel(SinePage, "sine", "Sine Wave"))
    app.add_channel(PageChannel(SinePage, "sine", "Sine Wave"))
