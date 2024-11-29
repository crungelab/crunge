from ...app import App

from ...page import Page, PageChannel

from imflodemo.nodes.volume import VolumeNode
from imflodemo.nodes.led import LedNode


class ConnectPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        VolumeNode(self.graph, "Volume")
        LedNode(self.graph, "Led")


def install(app: App):
    app.add_channel(PageChannel(ConnectPage, "connect", "Connect"))
