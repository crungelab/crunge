from typing import TYPE_CHECKING

from loguru import logger

from crunge import yoga

if TYPE_CHECKING:
    from ..window import Window

from ..viewport import Viewport
from . import Widget, Overlay


class Display(Widget):
    def __init__(self, overlays: list[Overlay] = None) -> None:
        style = yoga.StyleBuilder().size_percent(100, 100).build()
        super().__init__(style)
        self._window: "Window" = None
        self.viewport: Viewport = None
        self.overlays_by_name: dict[str, Overlay] = {}

        if overlays is None:
            overlays = []
        for overlay in overlays:
            self.add_overlay(overlay)

    @property
    def window(self) -> "Window":
        if self._window is None:
            from ..window import Window
            self._window = Window.get_current()

        return self._window

    """
    @property
    def viewport(self) -> Viewport:
        return self.window.viewport
    """

    def _create(self):
        super()._create()
        self.create_viewport()

    def create_viewport(self):
        self.viewport = self.window.viewport

    @property
    def overlays(self) -> list[Overlay]:
        return self.children
    
    def add_overlay(self, overlay: Overlay) -> Overlay:
        overlay.window = self.window
        self.overlays_by_name[overlay.name] = overlay
        #self.add_child(overlay) #TODO: I've got major lifecycle issues with this, so I'm going to try just adding it to the children list directly for now.
        self.children.append(overlay)
        self.sort_children(key=lambda child: child.priority)
        return overlay

    def remove_overlay(self, overlay: Overlay):
        self.overlays_by_name.pop(overlay.name)
        self.remove_child(overlay)

    def get_overlay(self, name: str) -> Overlay:
        return self.overlays_by_name[name]
