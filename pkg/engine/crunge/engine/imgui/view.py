from loguru import logger
import glm

from ..view import View

from .overlay import ImGuiOverlay

class ImGuiView(View):
    def __init__(self, layers=[]):
        super().__init__(layers=layers)
        self.gui: ImGuiOverlay = None

    def _create(self):
        super()._create()
        self.gui = ImGuiOverlay().config(view=self).create()
        self.add_layer(self.gui)
