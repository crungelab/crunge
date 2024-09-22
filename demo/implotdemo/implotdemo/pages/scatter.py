import numpy as np

from crunge import imgui
from crunge import implot
from crunge.engine import Renderer

from . import Page


class ScatterPlotPage(Page):
    def reset(self):
        self.a = np.random.rand(10)
        self.b = np.random.rand(10)

    def draw(self, renderer: Renderer):
        imgui.set_next_window_pos((16, 32), imgui.Cond.FIRST_USE_EVER )
        imgui.set_next_window_size((512, 512), imgui.Cond.FIRST_USE_EVER )

        imgui.begin(self.title)

        if implot.begin_plot("My Plot"):
            implot.plot_scatter("A", self.a, 10)
            implot.plot_scatter("B", self.b, 10)
            implot.end_plot()

        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(ScatterPlotPage, "scatter", "Scatter Plot")
