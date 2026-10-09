"""Signal: a lightweight observer primitive for node-level change notification.

Usage:
    transform_changed: Signal["Node"] = Signal()
    transform_changed.connect(chip.on_transform_changed)
    transform_changed.emit(node)

A chip that subscribes in `plug()` has missed everything emitted before it
was plugged. Use `connect_now` to subscribe and sync in one step:

    node.model_changed.connect_now(self.on_model_changed, node)
"""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

T = TypeVar("T")

__all__ = ["Signal", "Pulse"]

# Deferred mutation ops, applied once the outermost emit unwinds.
_CONNECT = 0
_DISCONNECT = 1
_CLEAR = 2


class Broadcast:
    """Subscription bookkeeping shared by Signal and Pulse.

    Mutating the subscriber list while an emit is in flight is deferred
    until the outermost emit returns, so a handler can disconnect itself,
    disconnect a sibling, or destroy the node that owns the signal without
    corrupting the iteration. Handlers already in the list still run for
    the emit in progress — disconnect takes effect from the next one.

    The deferral is what keeps emit allocation-free. Copying the list per
    emit would be simpler, but this fires on transform changes across every
    node in the scene and gen-0 pressure is not free under manual GC.
    """

    __slots__ = ("_subs", "_depth", "_pending")

    def __init__(self) -> None:
        self._subs: list[Callable] = []
        self._depth = 0
        self._pending: list[tuple[int, Callable | None]] | None = None

    # -- subscription ------------------------------------------------------

    def connect(self, fn: Callable) -> None:
        if self._depth:
            self._defer(_CONNECT, fn)
            return
        if fn not in self._subs:
            self._subs.append(fn)

    def disconnect(self, fn: Callable) -> bool:
        """Returns whether anything was actually removed.

        A False here usually means a handler was renamed and the connect
        side was updated but the disconnect side was not, or vice versa.
        Worth asserting on in code that should be symmetric.
        """
        if self._depth:
            self._defer(_DISCONNECT, fn)
            return fn in self._subs
        try:
            self._subs.remove(fn)
        except ValueError:
            return False
        return True

    def clear(self) -> None:
        if self._depth:
            self._defer(_CLEAR, None)
            return
        self._subs.clear()

    def is_connected(self, fn: Callable) -> bool:
        """Live state; ignores mutations deferred by an in-flight emit."""
        return fn in self._subs

    # -- deferral ----------------------------------------------------------

    def _defer(self, op: int, fn: Callable | None) -> None:
        if self._pending is None:
            self._pending = []
        self._pending.append((op, fn))

    def _flush(self) -> None:
        pending, self._pending = self._pending, None
        if pending is None:
            return
        for op, fn in pending:
            if op is _CONNECT:
                if fn not in self._subs:
                    self._subs.append(fn)
            elif op is _DISCONNECT:
                try:
                    self._subs.remove(fn)
                except ValueError:
                    pass
            else:
                self._subs.clear()

    # -- introspection -----------------------------------------------------

    def __len__(self) -> int:
        return len(self._subs)

    def __bool__(self) -> bool:
        return bool(self._subs)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} subs={len(self._subs)}>"


class Signal(Broadcast, Generic[T]):
    __slots__ = ()

    def connect(self, fn: Callable[[T], None]) -> None:
        super().connect(fn)

    def connect_now(self, fn: Callable[[T], None], value: T) -> None:
        """Connect, then call once with the current value.

        The caller supplies the value rather than the signal replaying a
        cached one: a cache would pin the last payload for the life of the
        signal, and the subscriber already knows where the state lives.
        """
        self.connect(fn)
        fn(value)

    def disconnect(self, fn: Callable[[T], None]) -> bool:
        return super().disconnect(fn)

    def emit(self, value: T) -> None:
        subs = self._subs
        if not subs:
            return
        self._depth += 1
        try:
            for fn in subs:
                fn(value)
        finally:
            self._depth -= 1
            if not self._depth and self._pending is not None:
                self._flush()


class Pulse(Broadcast):
    """Signal variant for events with no payload (e.g. per-frame pulses)."""

    __slots__ = ()

    def connect(self, fn: Callable[[], None]) -> None:
        super().connect(fn)

    def connect_now(self, fn: Callable[[], None]) -> None:
        self.connect(fn)
        fn()

    def disconnect(self, fn: Callable[[], None]) -> bool:
        return super().disconnect(fn)

    def emit(self) -> None:
        subs = self._subs
        if not subs:
            return
        self._depth += 1
        try:
            for fn in subs:
                fn()
        finally:
            self._depth -= 1
            if not self._depth and self._pending is not None:
                self._flush()