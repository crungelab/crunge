from loguru import logger

from ..view import View

from .layer import ImGuiLayer

class ImGuiView(View):
    def __init__(self, layers=[]):
        super().__init__(layers=layers)

    def create(self, window):
        super().create(window)
        self.add_layer(ImGuiLayer().create(self))
        return self