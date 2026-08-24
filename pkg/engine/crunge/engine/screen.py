from typing import TYPE_CHECKING

from loguru import logger

from .widget import Display, Overlay


class Screen(Display):
    def __init__(self, overlays: list[Overlay] = None) -> None:
        super().__init__(overlays)

    def _create(self):
        # logger.debug("Screen.create")
        super()._create()
