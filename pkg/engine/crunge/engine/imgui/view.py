from loguru import logger
import glm

from ..view import View

from .layer import ImGuiLayer

class ImGuiView(View):
    def __init__(self, size=glm.ivec2(), layers=[]):
        super().__init__(size, layers=layers)
        self.gui: ImGuiLayer = None

    def _create(self):
        super()._create()
        self.gui = ImGuiLayer().config(view=self).create()
        self.add_layer(self.gui)
        return self
