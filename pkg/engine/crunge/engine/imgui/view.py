from loguru import logger
import glm

from ..view import View

from .overlay import ImGuiOverlay

class ImGuiView(View):
    def __init__(self, overlays=[]):
        super().__init__(overlays=overlays)
        self.gui: ImGuiOverlay = None

    def _create(self):
        super()._create()
        self.gui = ImGuiOverlay().config(view=self).create()
        self.add_overlay(self.gui)
