from crunge import imgui

from imflo.page import Page

from imflodemo.nodes.volume import VolumeNode
from imflodemo.nodes.led import LedNode

class ConnectPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        VolumeNode(self.graph, 'Volume')
        LedNode(self.graph, 'Led')

def install(app):
    app.add_page(ConnectPage, "connect", "Connect")
