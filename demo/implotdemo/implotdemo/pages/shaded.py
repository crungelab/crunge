import numpy as np

from crunge import imgui
from crunge import implot

from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel

class ShadedPlotPage(Page):
    def reset(self):
        self.a = np.random.rand(10)
        self.b = np.random.rand(10)

    def _draw(self):
        imgui.begin(self.title)

        if implot.begin_plot("My Plot"):
            implot.plot_shaded("A", self.a, 10)
            implot.plot_shaded("B", self.b, 10)
            implot.end_plot()

        imgui.end()
        super()._draw()

def install(app):
    app.add_channel(PageChannel(ShadedPlotPage, "shaded", "Shaded Plot"))
