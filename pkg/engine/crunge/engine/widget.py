from __future__ import annotations

from loguru import logger
import glm

from crunge import yoga

from .sdl.event_handler import EventHandler
from .node import Node
from .layout import Layout
from crunge.core.dispatch import DispatchResult, EVENT_HANDLED, EVENT_UNHANDLED
from .gfx_access import GfxAccess


class WidgetLayout(Layout["Widget"]):
    """Widget-space layout: yoga's convention verbatim, y-down, integer pixels."""


class Widget(EventHandler, GfxAccess, Node["Widget"]):
    def __init__(self, style: yoga.Style = None, priority: int = 0, children: list["Widget"] = None) -> None:
        super().__init__(children=children)
        self.priority = priority
        self.hovered = False

        # Written only by the layout chip, through on_layout.
        self._position = glm.ivec2(0, 0)
        self._size = glm.ivec2(0, 0)

        self.layout = WidgetLayout(style)
        self.add_chip(self.layout)  # ASSUMPTION: node-side chip attachment method

    # -- geometry ----------------------------------------------------------
    #
    # Read-only by design. Geometry flows one way: style -> yoga -> here.
    # The setters raise rather than simply being absent, so the old call
    # sites surface with a message instead of silently writing a field
    # that the next apply() overwrites. Once the sweep is done these can
    # go and _position/_size can lose the prefix.

    @property
    def position(self) -> glm.ivec2:
        return self._position

    @position.setter
    def position(self, value: glm.ivec2) -> None:
        raise AttributeError(
            f"{type(self).__name__}.position is computed by the layout. "
            "Set it through the style, or read it after the next pass."
        )

    @property
    def size(self) -> glm.ivec2:
        return self._size

    @size.setter
    def size(self, value: glm.ivec2) -> None:
        raise AttributeError(
            f"{type(self).__name__}.size is computed by the layout. "
            "Use self.layout.set_size(x, y) instead."
        )

    @property
    def width(self) -> int:
        return self._size.x

    @width.setter
    def width(self, value: int) -> None:
        raise AttributeError(
            f"{type(self).__name__}.width is computed by the layout. "
            "Use self.layout.set_width(value) instead."
        )

    @property
    def height(self) -> int:
        return self._size.y

    @height.setter
    def height(self, value: int) -> None:
        raise AttributeError(
            f"{type(self).__name__}.height is computed by the layout. "
            "Use self.layout.set_height(value) instead."
        )

    @property
    def global_position(self) -> glm.ivec2:
        if self.parent is None:
            return glm.ivec2(0, 0)
        return self.parent.global_position + self._position

    @property
    def bounds(self) -> yoga.Bounds:
        return self.layout.bounds

    # -- layout ------------------------------------------------------------

    def on_layout(self, layout: Layout) -> None:
        position = glm.ivec2(layout.left, layout.top)
        size = glm.ivec2(layout.width, layout.height)

        changed = size != self._size
        self._position = position
        self._size = size

        if changed:
            self.on_size()

    def on_size(self) -> None:
        """Fires when the computed size changes. Same name and contract as
        the hook the old _set_size called."""

    @property
    def style(self) -> yoga.Style:
        return self.layout.style

    @style.setter
    def style(self, value: yoga.Style) -> None:
        self.layout.style = value

    # -- events ------------------------------------------------------------

    def dispatch(self, event) -> DispatchResult:
        for child in reversed(self.children):
            if child.dispatch(event):
                return EVENT_HANDLED
        return super().dispatch(event) or self.handle(event)

    def dispatch_2d(self, event, point) -> DispatchResult:
        for child in reversed(self.children):
            if child.dispatch_2d(event, point):
                return EVENT_HANDLED
        return super().dispatch_2d(event, point) or self.handle_2d(event, point)

    def hit_test(self, x: float, y: float) -> bool:
        position = self.global_position
        size = self._size
        if (
            position.x <= x <= position.x + size.x
            and position.y <= y <= position.y + size.y
        ):
            return True
        return False