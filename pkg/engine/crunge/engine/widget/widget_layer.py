from loguru import logger

from .. import Renderer

from ..view_layer import ViewLayer


class WidgetLayer(ViewLayer):
    def __init__(self):
        super().__init__("WidgetLayer", priority=950)

    def _draw(self) -> None:
        renderer = Renderer.get_current()

        with renderer.canvas_target() as canvas:
            super()._draw()
