from typing import TYPE_CHECKING

from loguru import logger

from crunge import yoga

if TYPE_CHECKING:
    from ..window import Window

from ..widget import Widget
from .overlay import Overlay


class View(Widget):
    def __init__(self, overlays: list[Overlay] = []) -> None:
        style = yoga.StyleBuilder().size_percent(100, 100).build()
        super().__init__(style)
        self.window: "Window" = None
        self.overlays_by_name: dict[str, Overlay] = {}

        for overlay in overlays:
            self.add_overlay(overlay)

    @property
    def overlays(self) -> list[Overlay]:
        return self.children

    def _create(self):
        #logger.debug("View.create")
        super()._create()
        if not self.window:
            raise ValueError("View.window is not set")
        for overlay in self.overlays:
            overlay.config(view=self).create()
        self.create_device_objects()
        self.create_camera()
        self.create_renderer()

    def create_device_objects(self):
        pass

    def create_camera(self):
        pass

    def create_renderer(self):
        pass

    def add_overlay(self, overlay: Overlay) -> Overlay:
        overlay.view = self
        self.overlays_by_name[overlay.name] = overlay
        self.add_child(overlay)
        self.sort_children(key=lambda child: child.priority)
        return overlay

    def remove_overlay(self, overlay: Overlay):
        overlay.view = None
        self.overlays_by_name.pop(overlay.name)
        self.remove_child(overlay)

    def get_overlay(self, name: str) -> Overlay:
        return self.overlays_by_name[name]
