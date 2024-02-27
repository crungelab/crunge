import numpy as np

from crunge import imgui
from crunge import implot
from crunge.engine import Renderer

from . import Page


class BarPlotPage(Page):
    def reset(self):
        self.a = np.random.rand(10)
        self.b = np.random.rand(10)

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        if implot.begin_plot("My Plot"):
            implot.plot_bars("A", self.a, 10)
            implot.plot_bars("B", self.b, 10)
            implot.end_plot()

        imgui.end()
        super().draw(renderer)

class BarPlotH(Page):
    def reset(self):
        self.a = np.random.rand(10)
        self.b = np.random.rand(10)

    def draw(self, renderer: Renderer):
        imgui.begin(self.title)

        if implot.begin_plot("My Plot"):
            implot.plot_bars_h("A", self.a, 10)
            implot.plot_bars_h("B", self.b, 10)
            implot.end_plot()

        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(BarPlotPage, "bar", "Bar Plot")
    app.add_page(BarPlotH, "bar_h", "Bar Plot - Horizontal")
