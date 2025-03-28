from collections import deque
import numpy as np

from crunge import imgui

from imflo.node import Node
from imflo.pin import Input

class ScopeNode(Node):
    def __init__(self, page):
        super().__init__(page)
        self.values = deque([0]*100, 100)
        self.input = Input(self, 'input', self.process)
        self.add_pin(self.input)

    def process(self, value):
        self.values.append(value)
        if len(self.values) > 100:
            self.values.popleft()

    def draw(self):
        imgui.begin("Scope")
        self.begin_input(self.input)
        imgui.button('input')
        self.end_input()
        imgui.same_line(spacing=16)
        imgui.plot_lines("Sin(t)", np.array(self.values).astype(np.float32), graph_size=imgui.get_content_region_avail())

        imgui.end()

