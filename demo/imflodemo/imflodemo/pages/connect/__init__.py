from crunge.engine import App
from crunge.demo import PageChannel

from imflodemo.nodes.volume import VolumeNode
from imflodemo.nodes.led import LedNode

from ...page import Page


class ConnectPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        VolumeNode(self.graph, "Volume")
        LedNode(self.graph, "Led")


def install(app: App):
    app.add_channel(PageChannel(ConnectPage, "connect", "Connect"))
