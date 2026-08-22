"""Signal: a lightweight observer primitive for node-level change notification.

Usage:
    transform_changed: Signal["Node"] = Signal()
    transform_changed.connect(chip._on_transform_change)
    transform_changed.emit(node)
"""

from __future__ import annotations

from typing import Callable, Generic, TypeVar

T = TypeVar("T")

__all__ = ["Signal"]


class Signal(Generic[T]):
    __slots__ = ("_subs",)

    def __init__(self) -> None:
        self._subs: list[Callable[[T], None]] = []

    def connect(self, fn: Callable[[T], None]) -> None:
        if fn not in self._subs:
            self._subs.append(fn)

    def disconnect(self, fn: Callable[[T], None]) -> None:
        try:
            self._subs.remove(fn)
        except ValueError:
            pass

    def emit(self, value: T) -> None:
        for fn in self._subs:
            fn(value)

    def clear(self) -> None:
        self._subs.clear()

    def __len__(self) -> int:
        return len(self._subs)

    def __bool__(self) -> bool:
        return bool(self._subs)


class Pulse:
    """Signal variant for events with no payload (e.g. per-frame pulses)."""

    __slots__ = ("_subs",)

    def __init__(self) -> None:
        self._subs: list[Callable[[], None]] = []

    def connect(self, fn: Callable[[], None]) -> None:
        if fn not in self._subs:
            self._subs.append(fn)

    def disconnect(self, fn: Callable[[], None]) -> None:
        try:
            self._subs.remove(fn)
        except ValueError:
            pass

    def emit(self) -> None:
        for fn in self._subs:
            fn()

    def clear(self) -> None:
        self._subs.clear()

    def __len__(self) -> int:
        return len(self._subs)

    def __bool__(self) -> bool:
        return bool(self._subs)
