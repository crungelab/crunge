from loguru import logger
import glm

from ..math import Size2i
from ..view import View

from .layer import ImGuiLayer

class ImGuiView(View):
    def __init__(self, size=Size2i(), layers=[]):
        super().__init__(size, layers=layers)
        self.gui: ImGuiLayer = None

    def _create(self, window):
        super()._create(window)
        self.gui = ImGuiLayer().create(self)
        self.add_layer(self.gui)
        return self
