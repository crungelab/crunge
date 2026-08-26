from __future__ import annotations

import threading
from enum import IntEnum
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Optional,
    Protocol,
    Tuple,
    runtime_checkable,
)

from loguru import logger

from .service import Service


class Phase(IntEnum):
    """
    Fixed ordering across phases, arbitrary ordering within a phase.
    Values are spaced so intermediate phases can be inserted without renumbering.
    """

    INPUT = 100
    BEHAVIOR = 200
    PHYSICS = 300
    ANIMATION = 400
    RESOLVE = 500  # transform + effective_visible resolution
    CAMERA = 600
    LATE = 700


UpdateFunc = Callable[[float], Any]


@runtime_checkable
class Updatable(Protocol):
    def update(self, delta_time: float) -> Any: ...


class Entry:
    """
    A registration handle. Holds the resolved callable so the per-frame loop
    never does attribute resolution on the target.
    """

    __slots__ = ("target", "func", "phase")

    def __init__(self, target: Any, func: UpdateFunc, phase: Phase):
        self.target = target
        self.func = func
        self.phase = phase

    @property
    def name(self) -> str:
        return getattr(self.target, "name", None) or type(self.target).__name__


class Updater(Service):
    _instance = None
    _lock = threading.Lock()  # For thread-safe singleton creation

    def __new__(cls, *args, **kwargs) -> "Updater":
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Updater, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self._initialized = True

        self.phases: Dict[Phase, List[Entry]] = {}
        self._sorted: Optional[List[List[Entry]]] = None

        # Deferred mutation, so register/unregister during update() is safe.
        self._iterating = False
        self._pending: List[Tuple[str, Any, Optional[Phase]]] = []

        # Game time, not wall time. Pausing the game pauses everything downstream.
        self.time_scale: float = 1.0
        self.elapsed: float = 0.0

    def register(self, target: Any, phase: Phase = Phase.BEHAVIOR) -> Entry:
        """
        Register an object with an `update(delta_time)` method, or a bare
        callable taking `delta_time`. Returns a handle usable with `remove`.
        """
        func = getattr(target, "update", None)
        if func is None:
            if not callable(target):
                raise TypeError(f"{target!r} is neither Updatable nor callable")
            func = target

        entry = Entry(target, func, phase)
        if self._iterating:
            self._pending.append(("add", entry, None))
        else:
            self._add(entry)
        return entry

    def unregister(self, target: Any, phase: Optional[Phase] = None) -> None:
        """
        Remove `target` from `phase`, or from every phase if `phase` is None.
        Accepts either the original target or the Entry returned by `register`.
        """
        if self._iterating:
            self._pending.append(("remove", target, phase))
        else:
            self._remove(target, phase)

    def clear(self) -> None:
        self.phases.clear()
        self._pending.clear()
        self._sorted = None
        logger.debug("Updater cleared.")

    def update(self, delta_time: float) -> None:
        """
        Run every registered updatable, phase by phase, in phase order.
        Allocates nothing on the hot path.
        """
        delta_time *= self.time_scale
        self.elapsed += delta_time

        if self._sorted is None:
            self._sorted = [self.phases[p] for p in sorted(self.phases)]

        self._iterating = True
        try:
            for bucket in self._sorted:
                for entry in bucket:
                    entry.func(delta_time)
        finally:
            self._iterating = False

        if self._pending:
            self._flush()

    def _add(self, entry: Entry) -> None:
        bucket = self.phases.get(entry.phase)
        if bucket is None:
            self.phases[entry.phase] = [entry]
            self._sorted = None
            logger.debug(f"Registered {entry.name} in phase {entry.phase.name}.")
            return

        for existing in bucket:
            if existing.target is entry.target:
                logger.warning(
                    f"{entry.name} already registered in phase {entry.phase.name}; ignoring."
                )
                return

        bucket.append(entry)
        logger.debug(f"Registered {entry.name} in phase {entry.phase.name}.")

    def _remove(self, target: Any, phase: Optional[Phase]) -> None:
        if isinstance(target, Entry):
            phase = target.phase if phase is None else phase
            target = target.target

        phases = (phase,) if phase is not None else tuple(self.phases)
        for p in phases:
            bucket = self.phases.get(p)
            if not bucket:
                continue
            for i, entry in enumerate(bucket):
                if entry.target is target:
                    del bucket[i]
                    logger.debug(f"Unregistered {entry.name} from phase {p.name}.")
                    break

    def _flush(self) -> None:
        pending, self._pending = self._pending, []
        for op, arg, phase in pending:
            if op == "add":
                self._add(arg)
            else:
                self._remove(arg, phase)
