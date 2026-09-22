"""Central hover tracking.

Widgets don't decide their own hover state. One tracker per root sees every
pointer move and the window-leave, hit-tests the tree, diffs against the
last result and sends on_exit / on_enter. A widget can't miss its exit
because an event was routed elsewhere or never arrived -- the tracker
doesn't depend on routing at all.

It also owns the cursor: the deepest hovered widget with a non-None
`cursor` wins, so two widgets can never fight over it on the same move.

Hover state and the cursor update on different schedules. Hover is
recomputed whenever asked, including from refresh() in the frame. The
cursor is only ever *set* from event handling (move, leave): SDL wants
cursor changes made there, and a set_cursor from the frame doesn't take.
refresh() just records the cursor it wants, and the next event applies it.
"""

from __future__ import annotations

from loguru import logger

from .widget import Widget
from .cursors import CURSOR_ARROW, set_cursor, get_cursor_name


def hover_path(widget: Widget, x: float, y: float) -> list[Widget]:
    """Root-to-leaf chain of widgets under the point, topmost branch only.

    Children are tried last-first, matching dispatch order, so of two
    overlapping siblings only the one drawn on top is hovered. A child
    outside its parent's bounds is unreachable, as if clipped.
    """
    if not widget.hit_test(x, y):
        return []
    for child in reversed(widget.children):
        path = hover_path(child, x, y)
        if path:
            return [widget, *path]
    return [widget]


class HoverTracker:
    def __init__(self, root: Widget) -> None:
        self.root = root
        self._hovered: list[Widget] = []
        self._point: tuple[float, float] | None = None
        # What the hovered widgets ask for vs. what SDL was last told.
        self._wanted = CURSOR_ARROW
        self._applied = None

    # -- event handling: hover and cursor ----------------------------------

    def move(self, x: float, y: float) -> None:
        """Pointer moved, in the root's coordinate space."""
        self._point = (x, y)
        self._update(hover_path(self.root, x, y))
        self._apply_cursor()

    def leave(self) -> None:
        """Pointer left the window: everything exits."""
        self._point = None
        self._update([])
        self._apply_cursor()

    # -- frame: hover only ---------------------------------------------------

    def refresh(self) -> None:
        """Re-hit-test at the last point, for when the tree moves under a
        stationary pointer -- after a layout apply, or a widget removal.

        Updates hover state now; a cursor change waits for the next event.
        """
        if self._point is not None:
            self._update(hover_path(self.root, *self._point))

    # -- internals -------------------------------------------------------------

    def _update(self, path: list[Widget]) -> None:
        # Identity, not equality: Node may define __eq__.
        old_ids = {id(w) for w in self._hovered}
        new_ids = {id(w) for w in path}

        # Exits deepest-first, enters outermost-first, as the DOM does.
        for widget in reversed(self._hovered):
            if id(widget) not in new_ids:
                logger.debug(f"Widget exited: {widget}")
                widget.hovered = False
                widget.on_exit()
        for widget in path:
            if id(widget) not in old_ids:
                logger.debug(f"Widget entered: {widget}")
                widget.hovered = True
                widget.on_enter()

        self._hovered = path

        self._wanted = next(
            (w.cursor for w in reversed(path) if w.cursor is not None),
            CURSOR_ARROW,
        )

    def _apply_cursor(self) -> None:
        #logger.debug(f"Applying cursor: wanted={self._wanted}, applied={self._applied}")

        if self._wanted is self._applied:
            return
        logger.debug(
            f"Cursor {get_cursor_name(self._applied)} -> {get_cursor_name(self._wanted)}"
        )
        # SDL3 returns bool; compare to False in case the binding returns None.
        if set_cursor(self._wanted) is False:
            # Leave _applied alone so the next event retries.
            logger.error(f"set_cursor({get_cursor_name(self._wanted)}) failed")
            return
        self._applied = self._wanted
