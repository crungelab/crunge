"""Tap behavior as a chip.

Any widget becomes clickable by seating one of these -- an Image, a Text, a
panel -- without a wrapper node in the tree and without the widget knowing
anything about input. Flutter needs GestureDetector to be a parent widget
because its widgets can't carry components; chips are exactly that, so the
behavior attaches to the widget it belongs to.

Press and release are tracked here, so a press that's dragged off cancels
instead of firing. That comes off the widget's hover state rather than a
per-chip hook: the tracker keeps `hovered` current wherever the pointer
goes, including out of the window.
"""

from __future__ import annotations

from typing import Callable, TYPE_CHECKING

from loguru import logger

from crunge import sdl

from ...controller import Controller
from ...cursor_chip import CursorChip

if TYPE_CHECKING:
    from ...widget import Widget


class GestureChip(Controller["Widget"]):
    def __init__(self, on_tap: Callable[[], None] | None = None) -> None:
        super().__init__()
        self.on_tap = on_tap
        self.pressed = False

    @property
    def interactive(self) -> bool:
        """Flutter's rule: no callback means it ignores input."""
        return self.on_tap is not None

    def _create(self):
        super()._create()
        if self.node.get_chip(CursorChip) is None:
            self.node.add_chip(CursorChip())

    # -- hover -------------------------------------------------------------

    def plug(self) -> None:
        self.node.hover_changed.connect(self.on_hover_changed)

    def unplug(self) -> None:
        self.node.hover_changed.disconnect(self.on_hover_changed)

    def on_hover_changed(self, widget: "Widget") -> None:
        if not widget.hovered:
            # Dragged off, or the pointer left the window: cancel the press.
            # The release may never be routed here, so this is the only
            # notice we get.
            self.pressed = False

    # -- input -------------------------------------------------------------

    def on_mouse_button(self, event: sdl.MouseButtonEvent):
        super().on_mouse_button(event)
        logger.debug(f"interactive={self.interactive}")
        if not self.interactive or event.button != 1:  # left button only
            return False

        inside = self.node.hit_test(event.x, event.y)
        logger.debug(f"Mouse button event at ({event.x}, {event.y}), inside={inside}")
        if event.down:
            self.pressed = inside
            return inside

        # Fire on release inside, like Flutter: dragging off cancels.
        was_pressed = self.pressed
        self.pressed = False
        if was_pressed and inside:
            logger.debug(f"{type(self).__name__} pressed at ({event.x}, {event.y})")
            self.on_tap()
            return True
        return False
