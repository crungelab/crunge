from loguru import logger
import glm

from ..screen import Screen

from .overlay import ImGuiOverlay

class ImGuiScreen(Screen):
    def __init__(self, overlays=None):
        super().__init__(overlays=overlays)
        self.gui: ImGuiOverlay = None

    def _create(self):
        super()._create()
        self.gui = ImGuiOverlay()
        self.add_overlay(self.gui)
