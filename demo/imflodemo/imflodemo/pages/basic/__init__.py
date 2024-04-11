from crunge import imgui, imnodes

from imflo.page import Page

from imflodemo.nodes.volume import VolumeNode
from imflodemo.nodes.led import LedNode
from imflo.wire import Wire

class BasicPage(Page):
    def __init__(self, name, title):
        super().__init__(name, title)
        volume_node = VolumeNode(self.graph, 'Volume')
        led_node = LedNode(self.graph, 'Led')
        self.graph.add_wire(Wire(volume_node.get_pin('output'), led_node.get_pin('input')))

def install(app):
    app.add_page(BasicPage, "basic", "Basic")
