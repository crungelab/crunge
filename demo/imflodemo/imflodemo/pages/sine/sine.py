import numpy as np
from rx.subject import Subject

from crunge import imgui

from imflo.node import Node
from imflo.pin import Output

sampling_rate = 44100
freq = 440
samples = 44100


class SineNode(Node):
    def __init__(self, page):
        super().__init__(page)
        self._freq = 88
        self.clock = 0
        self.subject = Subject()
        self.output = Output(self, 'output', self.subject)
        self.add_pin(self.output)

    @property
    def freq(self):
        return self._freq

    @freq.setter
    def freq(self, value):
        self._freq = value

    def update(self, delta_time):
        self.clock = self.clock + delta_time
        x = self.clock
        y = np.sin(self.freq * x)
        self.output.write(y)
    
    def draw(self):
        width = 20
        height = 100

        imgui.set_next_window_size((160, 160), imgui.Cond.ONCE)

        imgui.begin("Sin")
        changed, freq = imgui.v_slider_int(
            "freq",
            (width, height), self.freq,
            v_min=0, v_max=100,
            format="%d"
        )
        if changed:
            self.freq = freq

        imgui.same_line(spacing=16)
        self.begin_output(self.output)
        imgui.button('output')
        self.end_output()

        imgui.end()

