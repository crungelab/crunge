from loguru import logger

from crunge.engine.imgui import ImGuiView
#from crunge.engine.view import View

from .trial_layer import TrialLayer


class TrialView(ImGuiView):
#class TrialView(View):
    def __init__(self, layers=[]):
        super().__init__(layers=layers)
        
    def _create(self):
        super()._create()
        widget_layer = TrialLayer()
        self.add_layer(widget_layer)
        self.ui = widget_layer
