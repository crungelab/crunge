from loguru import logger
import glm

from ..view import View

from .layer import ImGuiLayer

class ImGuiView(View):
    def __init__(self, size=glm.ivec2(), layers=[]):
        super().__init__(size, layers=layers)

    def create(self, window):
        super().create(window)
        self.add_layer(ImGuiLayer().create(self))
        return self