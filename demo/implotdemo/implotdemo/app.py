from pathlib import Path

from crunge import implot
from crunge import demo

resource_root = Path(__file__).parent.parent / 'resources'

class ImPlotDemo(demo.Demo):
    def __init__(self):
        super().__init__("ImPlot Demo", __package__, resource_root)
        implot.create_context()

