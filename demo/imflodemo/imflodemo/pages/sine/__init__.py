from crunge.engine import Renderer, App
from crunge.demo import PageChannel

from imflodemo.nodes.sine import SineNode
from imflodemo.nodes.scope import ScopeNode

from ...page import Page


class SinePage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        SineNode(self.graph, "Sin")
        ScopeNode(self.graph, "Scope")


def install(app: App):
    app.add_channel(PageChannel(SinePage, "sine", "Sine Wave"))
