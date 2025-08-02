import numpy as np

from crunge import imgui
from crunge import implot

from crunge.engine import Renderer, App
from crunge.demo import Page, PageChannel


class ScatterPlotPage(Page):
    def reset(self):
        self.a = np.random.rand(10)
        self.b = np.random.rand(10)

    def _draw(self):
        imgui.set_next_window_pos((16, 32), imgui.Cond.FIRST_USE_EVER )
        imgui.set_next_window_size((512, 512), imgui.Cond.FIRST_USE_EVER )

        imgui.begin(self.title)

        if implot.begin_plot("My Plot"):
            implot.plot_scatter("A", self.a, 10)
            implot.plot_scatter("B", self.b, 10)
            implot.end_plot()

        imgui.end()
        super()._draw()

def install(app: App):
    app.add_channel(PageChannel(ScatterPlotPage, "scatter", "Scatter Plot"))
