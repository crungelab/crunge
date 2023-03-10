import numpy as np

from crunge import imgui
from crunge import implot

from . import Page


class LinePlotPage(Page):
    def reset(self):
        self.a = np.random.rand(10)
        self.b = np.random.rand(10)

    def draw(self):
        imgui.set_next_window_pos((16, 32), imgui.COND_FIRST_USE_EVER )
        imgui.set_next_window_size((512, 512), imgui.COND_FIRST_USE_EVER )

        imgui.begin(self.title)

        if implot.begin_plot("My Plot"):
            implot.plot_line("A", self.a, 10)
            implot.plot_line("B", self.b, 10)
            #implot.plot_bars("B", self.values, 10)
            implot.end_plot()

        imgui.end()

def install(app):
    app.add_page(LinePlotPage, "line", "Line Plot")
