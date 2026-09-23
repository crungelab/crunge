"""Task scheduler.

By default delays and intervals are measured in real time (time.perf_counter),
so they are correct no matter how often ``update`` is called or what units the
caller's ``delta_time`` is in. Set ``Scheduler.use_game_time = True`` to measure
them in accumulated ``delta_time`` instead (pauses with the game loop, but only
correct if ``update`` is called exactly once per frame with seconds).

Callbacks receive ``elapsed`` as their first argument: the game time since the
task last ran, or since it was scheduled if it hasn't run yet. So
``schedule_once(f, 2.0)`` calls ``f(~2.0)``.
"""
from __future__ import annotations

import heapq
import time
import itertools
import threading
from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from loguru import logger

from .service import Service


TaskFunc = Callable[..., Any]


def _func_name(func: TaskFunc) -> str:
    # functools.partial and callable objects have no __name__.
    return getattr(func, "__qualname__", None) or getattr(func, "__name__", None) or repr(func)


@dataclass(eq=False)
class Task:
    func: TaskFunc
    next_run: float                   # Scheduler time when the task is next due
    interval: Optional[float] = None  # None for one-shot tasks
    args: tuple = ()
    kwargs: dict = field(default_factory=dict)
    last_run: float = 0.0             # Scheduler time of last run (or of scheduling)
    seq: int = 0                      # Tie-breaker: equal due times run in FIFO order
    cancelled: bool = False           # Also set once a one-shot task has finished

    @property
    def repeat(self) -> bool:
        return self.interval is not None

    @property
    def name(self) -> str:
        return _func_name(self.func)

    def cancel(self) -> None:
        """Cancel this task. Safe to call from any callback, including its own."""
        self.cancelled = True

    def __lt__(self, other: "Task") -> bool:
        return (self.next_run, self.seq) < (other.next_run, other.seq)


class Scheduler(Service):
    _instance: Optional["Scheduler"] = None
    _instance_lock = threading.Lock()  # For thread-safe singleton creation
    use_game_time = False

    def __new__(cls, *args: Any, **kwargs: Any) -> "Scheduler":
        with cls._instance_lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if getattr(self, "_initialized", False):
            return
        self._initialized = True
        self._time = 0.0
        self._queue: list[Task] = []   # Min-heap ordered by (next_run, seq)
        self._due: list[Task] = []     # Tasks popped and being run in the current update
        self._counter = itertools.count()
        self._lock = threading.RLock()

    # ------------------------------------------------------------------ info

    @property
    def now(self) -> float:
        """Current scheduler time in seconds."""
        return self._time if self.use_game_time else time.perf_counter()

    def __len__(self) -> int:
        with self._lock:
            return sum(1 for t in itertools.chain(self._queue, self._due) if not t.cancelled)

    # ------------------------------------------------------------ scheduling

    def schedule(self, func: TaskFunc, interval: float, *args: Any, **kwargs: Any) -> Task:
        """
        Call `func(elapsed, *args, **kwargs)` every `interval` seconds of game time.
        Returns the Task, which can be cancelled with `task.cancel()`.
        """
        if interval <= 0:
            raise ValueError(f"interval must be > 0, got {interval}")
        task = self._add(func, interval, interval, args, kwargs)
        logger.debug(f"Scheduled repeating task {task.name} every {interval}s.")
        return task

    def schedule_once(self, func: TaskFunc, delay: float = 0.0, *args: Any, **kwargs: Any) -> Task:
        """
        Call `func(elapsed, *args, **kwargs)` once after `delay` seconds of game time.
        A delay of 0 runs on the next update.
        Returns the Task, which can be cancelled with `task.cancel()`.
        """
        if delay < 0:
            raise ValueError(f"delay must be >= 0, got {delay}")
        task = self._add(func, delay, None, args, kwargs)
        logger.debug(f"Scheduled one-time task {task.name} after {delay}s.")
        return task

    def _add(
        self,
        func: TaskFunc,
        delay: float,
        interval: Optional[float],
        args: tuple,
        kwargs: dict,
    ) -> Task:
        with self._lock:
            now = self.now
            task = Task(
                func=func,
                next_run=now + delay,
                interval=interval,
                args=args,
                kwargs=kwargs,
                last_run=now,
                seq=next(self._counter),
            )
            heapq.heappush(self._queue, task)
        return task

    def unschedule(self, func: TaskFunc) -> int:
        """
        Cancel every pending task for `func`. Returns how many were cancelled.
        Uses == so bound methods match (obj.method is not obj.method, but they compare equal).
        """
        with self._lock:
            count = 0
            for task in itertools.chain(self._queue, self._due):
                if not task.cancelled and task.func == func:
                    task.cancelled = True
                    count += 1
            if count:
                self._queue = [t for t in self._queue if not t.cancelled]
                heapq.heapify(self._queue)
        if count:
            logger.debug(f"Unscheduled {count} task(s) for {_func_name(func)}.")
        return count

    def clear(self) -> None:
        """Cancel all tasks."""
        with self._lock:
            for task in itertools.chain(self._queue, self._due):
                task.cancelled = True
            self._queue.clear()

    # ---------------------------------------------------------------- update

    def update(self, delta_time: float) -> None:
        """Advance scheduler time by `delta_time` and run every task that is due."""
        with self._lock:
            if self.use_game_time:
                self._time += delta_time
            now = self.now
            due: list[Task] = []
            while self._queue and self._queue[0].next_run <= now:
                task = heapq.heappop(self._queue)
                if not task.cancelled:
                    due.append(task)
            self._due = due

        # Callbacks run outside the lock so they can schedule/unschedule freely.
        # Anything they schedule goes into the queue and runs on a later update,
        # so a zero-delay task that reschedules itself can't spin forever.
        try:
            for task in due:
                if task.cancelled:  # Cancelled by an earlier callback this frame
                    continue

                elapsed = now - task.last_run
                task.last_run = now
                try:
                    task.func(elapsed, *task.args, **task.kwargs)
                except Exception:
                    logger.exception(f"Scheduled task {task.name} raised; unscheduling it.")
                    task.cancelled = True
                    continue

                if not task.repeat:
                    task.cancelled = True  # Finished
                elif not task.cancelled:
                    # Fixed-rate: step from the previous due time so the interval
                    # doesn't drift by a frame each run. If we've fallen more than
                    # an interval behind, skip the missed runs rather than bursting.
                    task.next_run += task.interval
                    if task.next_run <= now:
                        task.next_run = now + task.interval
                    with self._lock:
                        heapq.heappush(self._queue, task)
        finally:
            with self._lock:
                self._due = []
