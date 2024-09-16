import time
import threading
from typing import Callable, Any, List, Optional

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

class Scheduler:
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
        print(f"Scheduled repeating task {func.__name__} every {interval} seconds.")

    def schedule_once(self, func: Callable[[float], Any], delay: float) -> None:
        """
        Schedule a function to be called once after `delay` seconds.
        The function will receive `delta_time` as an argument.
        """
        next_run = time.time() + delay
        task = Task(func, next_run, repeat=False)
        self.tasks.append(task)
        print(f"Scheduled one-time task {func.__name__} after {delay} seconds.")

    def update(self, delta_time: float) -> None:
        """
        Process scheduled tasks and execute any that are due.
        Passes `delta_time` to each scheduled function.
        """
        now = time.time()
        for task in self.tasks[:]:  # Iterate over a copy of the list
            if now >= task.next_run:
                delta_time = now - (task.last_run if task.last_run is not None else task.next_run - (task.interval if task.interval else 0))
                task.last_run = now
                print(f"Executing task {task.func.__name__} with delta_time {delta_time:.2f}s")
                task.func(delta_time)
                if task.repeat and task.interval is not None:
                    task.next_run = now + task.interval
                    print(f"Rescheduled repeating task {task.func.__name__}")
                else:
                    self.tasks.remove(task)
                    print(f"Removed one-time task {task.func.__name__}")

'''
# Example usage:
if __name__ == "__main__":
    scheduler = Scheduler()

    def say_hello(delta_time: float) -> None:
        print(f"Hello, world! Delta time since last call: {delta_time:.2f}s")

    def say_goodbye(delta_time: float) -> None:
        print(f"Goodbye, world! Delta time since last call: {delta_time:.2f}s")

    # Schedule tasks
    scheduler.schedule(say_hello, interval=5.0)    # Repeats every 5 seconds
    scheduler.schedule_once(say_goodbye, delay=10.0)  # Executes once after 10 seconds

    # Main loop
    try:
        while True:
            scheduler.update()
            time.sleep(1)  # Sleep to prevent high CPU usage
    except KeyboardInterrupt:
        print("Scheduler stopped.")
'''