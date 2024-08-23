import os
import random

from crunge import imgui

from imflo.particle import AnimatedAlphaParticle

from imflo.page import Page

from imflodemo.nodes.sine import SineNode
from imflodemo.nodes.scope import ScopeNode
from imflodemo.nodes.spark import SparkNode

class SparksPage(Page):
    def __init__(self, window, name, title):
        super().__init__(window, name, title)
        sine_node = SineNode(self.graph, 'Sine')
        scope_node = ScopeNode(self.graph, 'Scope')
        spark_node = SparkNode(self.graph, 'Spark')
        self.graph.connect(sine_node.get_pin('output'), scope_node.get_pin('input'))
        self.graph.connect(sine_node.get_pin('output'), spark_node.get_pin('input'))

    def reset(self):
        super().reset()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

def install(app):
    app.add_page(SparksPage, "sparks", "Sparks")
