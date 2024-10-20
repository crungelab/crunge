from array import array
from collections import deque
from random import random
from math import sin
import numpy as np

from crunge import imgui

from imflo.node import Node
from imflo.pin import Input

class ScopeNode(Node):
    def __init__(self, graph, name):
        super().__init__(graph, name)
        #self.values = array('f', [sin(x * 0.1) for x in range(100)])
        self.values = deque([0]*100, 100)
        self.input = Input(self, 'input', self.process)

    def process(self, value):
        self.values.append(value)
        if len(self.values) > 100:
            self.values.popleft()

    def begin(self):
        super().begin()
        #imgui.plot_lines("Sin(t)", np.array(self.values).astype(np.float32), graph_size=imgui.get_content_region_avail())
        imgui.plot_lines("Sin(t)", np.array(self.values).astype(np.float32))
