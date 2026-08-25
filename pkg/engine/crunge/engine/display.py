from typing import TYPE_CHECKING

from loguru import logger

from crunge import yoga

if TYPE_CHECKING:
    from .window import Window
    from .view import View

from .d2.camera_2d import Camera2D
from .d3.camera_3d import Camera3D
from .d3.lighting_3d import Lighting3D

from .viewport import Viewport
from .widget import Widget, Overlay

class Display(Widget):
    def __init__(self, name: str = "Display", title: str = "Display", overlays: list[Overlay] = None, views: list["View"] = None) -> None:
        self.name = name
        self.title = title
        # Buckets must exist before any add_* call below.
        self._overlays: list[Overlay] = []
        self._views: list["View"] = []
        self._window: "Window" = None
        self.viewport: Viewport = None

        style = yoga.StyleBuilder().size_percent(100, 100).build()
        super().__init__(style)

        for overlay in overlays or ():
            self.add_overlay(overlay)
        for view in views or ():
            self.add_view(view)

    @property
    def window(self) -> "Window":
        if self._window is None:
            from .window import Window
            self._window = Window.get_current()
        return self._window

    @window.setter
    def window(self, value: "Window") -> None:
        self._window = value

    # --- children -----------------------------------------------------

    def on_child_added(self, child: Widget) -> None:
        from .view import View
        if isinstance(child, View):
            self._views.append(child)
        elif isinstance(child, Overlay):
            self._overlays.append(child)
        self.sort_children(key=lambda child: child.priority)
        logger.debug(f"{self.name}: on_child_added: {child.name} ({type(child).__name__}, priority={child.priority})")

    def on_child_removed(self, child: Widget) -> None:
        from .view import View
        if isinstance(child, View):
            self._views.remove(child)
        elif isinstance(child, Overlay):
            self._overlays.remove(child)
        self.sort_children(key=lambda child: child.priority)

    @property
    def overlays(self) -> list[Overlay]:
        return self._overlays

    @property
    def views(self) -> list["View"]:
        return self._views

    @property
    def primary_view(self) -> "View":
        raise NotImplementedError(f"{self.name}: primary_view")

    @property
    def primary_camera_2d(self) -> Camera2D:
        raise NotImplementedError(f"{self.name}: primary_camera_2d")

    @property
    def primary_camera_3d(self) -> Camera3D:
        raise NotImplementedError(f"{self.name}: primary_camera_3d")

    @property
    def primary_lighting_3d(self) -> Lighting3D:
        raise NotImplementedError(f"{self.name}: primary_lighting_3d")

    def add_overlay(self, overlay: Overlay) -> Overlay:
        overlay.window = self.window
        return self.add_child(overlay)

    def remove_overlay(self, overlay: Overlay) -> None:
        self.remove_child(overlay)

    def get_overlay(self, name: str) -> Overlay:
        return self._children_by_name[name]

    def add_view(self, view: "View") -> "View":
        return self.add_child(view)

    def remove_view(self, view: "View") -> None:
        self.remove_child(view)

    def get_view(self, name: str) -> "View":
        return self._children_by_name[name]

    # --- lifecycle ----------------------------------------------------

    def _create(self):
        super()._create()
        self.create_viewport()
        self.create_children()

    def create_viewport(self):
        self.viewport = self.window.viewport

    def create_children(self):
        pass