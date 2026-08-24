from typing import TYPE_CHECKING

from loguru import logger

from .widget import Display, Overlay
from .view import View


class Screen(Display):
    def __init__(self, overlays: list[Overlay] = None) -> None:
        super().__init__(overlays)
        self.view: View = None

    def _create(self):
        # logger.debug("Screen.create")
        super()._create()
        self.create_children()

    def create_children(self):
        pass