import sys, os
#sys.setdlopenflags(os.RTLD_GLOBAL | os.RTLD_LAZY)

import numpy as np

import arcade

from crunge import imgui
from crunge.imgui.impl.arcade import ArcadeGui

from crunge import implot

class MyGui(ArcadeGui):
    def __init__(self, window):
        super().__init__(window)
        implot.create_context()


class App(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "Main Window", resizable=True)
        self.gui = MyGui(self)
        self.a = np.random.rand(10)
        self.b = np.random.rand(10)

    def on_draw(self):
        arcade.start_render()
        imgui.new_frame()

        imgui.set_next_window_pos((16, 32), imgui.COND_FIRST_USE_EVER )
        imgui.set_next_window_size((512, 512), imgui.COND_FIRST_USE_EVER )

        imgui.begin('Line Plot')

        if implot.begin_plot("My Plot"):
            implot.plot_line("A", self.a, 10)
            implot.plot_line("B", self.b, 10)
            #implot.plot_bars("B", self.values, 10)
            implot.end_plot()

        imgui.end()
        #imgui.show_metrics_window()
        imgui.end_frame()
        self.gui.render()

app = App()

arcade.run()
