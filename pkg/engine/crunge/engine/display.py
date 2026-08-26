from typing import TYPE_CHECKING, Iterable

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
from .overlay.overlay_manufacturer import OverlayManufacturer, OverlayConfig

from .d2.overlay.scratch_overlay import ScratchOverlay
from .imgui.overlay import ImGuiOverlay


class Display(Widget):
    default_overlays: tuple[OverlayConfig, ...] = ()

    def __init__(
        self,
        name: str = "Display",
        title: str = "Display",
        overlays: Iterable[OverlayConfig] = None,
    ) -> None:
        self.name = name
        self.title = title

        self.viewport: Viewport = None

        # Buckets must exist before super().__init__ touches children.
        self._overlays: list[Overlay] = []
        self._views: list["View"] = []
        self._window: "Window" = None

        self.overlay_manufacturer = OverlayManufacturer(
            self.default_overlays if overlays is None else overlays
        )

        style = yoga.StyleBuilder().size_percent(100, 100).build()
        super().__init__(style)

        self._scratch: ScratchOverlay = None
        self._gui: ImGuiOverlay = None


    @property
    def scratch(self) -> ScratchOverlay:
        if self._scratch is None:
            self._scratch = ScratchOverlay()
            self.add_overlay(self._scratch)
        return self._scratch

    @property
    def gui(self) -> ImGuiOverlay:
        if self._gui is None:
            self._gui = ImGuiOverlay()
            self.add_overlay(self._gui)
        return self._gui

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
            self._views.sort(key=lambda c: c.priority)
        elif isinstance(child, Overlay):
            self._overlays.append(child)
            self._overlays.sort(key=lambda c: c.priority)
        self.sort_children(key=lambda c: c.priority)
        logger.debug(
            f"{self.name}: on_child_added: {child.name} "
            f"({type(child).__name__}, priority={child.priority})"
        )

    def on_child_removed(self, child: Widget) -> None:
        from .view import View

        if isinstance(child, View) and child in self._views:
            self._views.remove(child)
        elif isinstance(child, Overlay) and child in self._overlays:
            self._overlays.remove(child)

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
        overlay.display = self
        return self.add_child(overlay)

    def remove_overlay(self, overlay: Overlay) -> None:
        self.remove_child(overlay)

    def get_overlay(self, name: str) -> Overlay | None:
        for overlay in self._overlays:
            if overlay.name == name:
                return overlay
        return None

    def add_view(self, view: "View") -> "View":
        return self.add_child(view)

    def remove_view(self, view: "View") -> None:
        self.remove_child(view)

    def get_view(self, name: str) -> "View | None":
        for view in self._views:
            if view.name == name:
                return view
        return None

    def toggle_overlay(self, name: str) -> Overlay | None:
        overlay = self.get_overlay(name)
        if overlay is not None:
            self.remove_overlay(overlay)
            return None
        overlay = self.overlay_manufacturer.manufacture(name)
        if overlay is not None:
            self.add_overlay(overlay)
        return overlay

    # --- lifecycle ----------------------------------------------------

    def _create(self):
        super()._create()
        self.create_viewport()
        self.create_views()
        self.create_overlays()

    def create_viewport(self):
        self.viewport = self.window.viewport

    def create_views(self):
        pass

    def create_overlays(self):
        for overlay in self.overlay_manufacturer.manufacture_all():
            self.add_overlay(overlay)
