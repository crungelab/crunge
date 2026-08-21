from loguru import logger

from crunge.engine.imgui import ImGuiView

from .trial_overlay import TrialOverlay


class TrialView(ImGuiView):
    def __init__(self, overlays=[]):
        super().__init__(overlays=overlays)
        
    def _create(self):
        super()._create()
        widget_overlay = TrialOverlay()
        self.add_overlay(widget_overlay)
        self.ui = widget_overlay
