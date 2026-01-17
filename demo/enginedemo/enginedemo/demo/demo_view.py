from loguru import logger

from crunge.engine.imgui import ImGuiView

class DemoView(ImGuiView):
    def __init__(self, overlays=[]):
        super().__init__(overlays=overlays)
