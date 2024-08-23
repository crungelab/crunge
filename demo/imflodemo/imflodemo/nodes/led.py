from array import array
from random import random
from math import sin

from crunge import imgui, imnodes

from imflo.node import Node
from imflo.pin import Input

class LedNode(Node):
    def __init__(self, graph, name):
        super().__init__(graph, name)
        self.value = 0
        self.input = Input(self, 'input', self.process)

    def process(self, value):
        self.value = value

    def begin(self):
        super().begin()
        imgui.text(str(self.value))

