from loguru import logger

from .. import Renderer

from ..view.overlay import Overlay


class WidgetOverlay(Overlay):
    def __init__(self):
        super().__init__("WidgetOverlay", priority=950)

    def _draw(self) -> None:
        renderer = Renderer.get_current()

        with renderer.canvas_target() as canvas:
            super()._draw()
