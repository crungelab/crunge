import time
import threading
from typing import Callable, Any, List, Optional

from loguru import logger

from .service import Service


class Task:
    def __init__(
        self,
        func: Callable[[float], Any],
        next_run: float,
        interval: Optional[float] = None,
        repeat: bool = False,
        last_run: Optional[float] = None,
    ):
        self.func = func
        self.next_run = next_run  # Timestamp when the task should run next
        self.interval = interval  # Interval in seconds
        self.repeat = repeat      # True if the task should repeat
        self.last_run = last_run  # Timestamp when the task was last run

class Scheduler(Service):
    _instance = None
    _lock = threading.Lock()  # For thread-safe singleton creation

    def __new__(cls, *args, **kwargs) -> 'Scheduler':
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Scheduler, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if hasattr(self, '_initialized') and self._initialized:
            return
        self._initialized = True
        self.tasks: List[Task] = []

    def schedule(self, func: Callable[[float], Any], interval: float) -> None:
        """
        Schedule a function to be called every `interval` seconds.
        The function will receive `delta_time` as an argument.
        """
        next_run = time.time() + interval
        task = Task(func, next_run, interval=interval, repeat=True)
        self.tasks.append(task)
        logger.debug(f"Scheduled repeating task {func.__name__} every {interval} seconds.")

    def schedule_once(self, func: Callable[[float], Any], delay: float = 0.0) -> None:
        """
        Schedule a function to be called once after `delay` seconds.
        The function will receive `delta_time` as an argument.
        """
        next_run = time.time() + delay
        task = Task(func, next_run, repeat=False)
        self.tasks.append(task)
        logger.debug(f"Scheduled one-time task {func.__name__} after {delay} seconds.")

    def update(self, delta_time: float) -> None:
        #logger.debug(f"Scheduler update called with delta_time: {delta_time:.2f}s")
        """
        Process scheduled tasks and execute any that are due.
        Passes `delta_time` to each scheduled function.
        """
        now = time.time()
        for task in self.tasks[:]:  # Iterate over a copy of the list
            if now >= task.next_run:
                delta_time = now - (task.last_run if task.last_run is not None else task.next_run - (task.interval if task.interval else 0))
                task.last_run = now
                logger.debug(f"Executing task {task.func.__name__} with delta_time {delta_time:.2f}s")
                task.func(delta_time)
                if task.repeat and task.interval is not None:
                    task.next_run = now + task.interval
                    logger.debug(f"Rescheduled repeating task {task.func.__name__}")
                else:
                    self.tasks.remove(task)
                    logger.debug(f"Removed one-time task {task.func.__name__}")
