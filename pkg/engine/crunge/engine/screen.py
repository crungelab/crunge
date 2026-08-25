from typing import TYPE_CHECKING

from loguru import logger

from .widget import Overlay
from .display import Display
from .view import View


class Screen(Display):
    def __init__(self, name: str = "Screen", title: str = "Screen", overlays: list[Overlay] = None) -> None:
        super().__init__(name=name, title=title, overlays=overlays)
        self._primary_view: "View" = None

    @property
    def primary_view(self) -> "View":
        if self._primary_view is not None:
            return self._primary_view
        if not self._views:
            raise ValueError(f"{self.name}: no views")
        return self._views[0]
