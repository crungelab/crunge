from loguru import logger

from .. import Renderer

from ..overlay.overlay import Overlay


class UiOverlay(Overlay):
    def __init__(self, name: str = "UiOverlay"):
        super().__init__(name, priority=950)

    def _draw(self) -> None:
        renderer = Renderer.get_current()

        with renderer.canvas_target() as canvas:
            super()._draw()
