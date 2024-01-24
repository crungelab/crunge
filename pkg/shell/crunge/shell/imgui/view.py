from loguru import logger

from ..view import View

from .layer import ImGuiLayer

class ImGuiView(View):
    def __init__(self, window):
        super().__init__(window)
        logger.debug("ImGuiView.__init__")
        self.add_layer(ImGuiLayer(self))