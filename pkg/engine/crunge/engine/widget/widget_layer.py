from loguru import logger

from .. import Renderer

from ..view_layer import ViewLayer


class WidgetLayer(ViewLayer):
    def __init__(self):
        super().__init__("WidgetLayer", priority=950)

    def draw(self, renderer: Renderer) -> None:
        with renderer.canvas_target() as canvas:
            super().draw(renderer)
