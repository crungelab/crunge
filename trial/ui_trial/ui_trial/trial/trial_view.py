from loguru import logger

from crunge.engine.imgui import ImGuiView

from .trial_layer import TrialLayer


class TrialView(ImGuiView):
    def __init__(self, layers=[]):
        super().__init__(layers=layers)
        widget_layer = TrialLayer()
        self.add_layer(widget_layer)
        self.ui = widget_layer
        
