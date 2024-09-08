from loguru import logger
import glm

from ..view import View

from .layer import ImGuiLayer

class ImGuiView(View):
    def __init__(self, size=glm.ivec2(), layers=[]):
        super().__init__(size, layers=layers)
        self.gui: ImGuiLayer = None

    def _create(self, window):
        super()._create(window)
        self.gui = ImGuiLayer().create(self)
        self.add_layer(self.gui)
        return self

    '''
    def create(self, window):
        super().create(window)
        self.gui = ImGuiLayer().create(self)
        self.add_layer(self.gui)
        return self
    '''