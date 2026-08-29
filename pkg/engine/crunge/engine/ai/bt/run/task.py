from typing import TYPE_CHECKING, Any, Callable, List, Optional, Coroutine

if TYPE_CHECKING:
    from .bot import Bot

import enum
import types
import inspect
import traceback
from uuid import uuid1

from loguru import logger

from ..utils import singleton
from ..run import Message
from .policy import Policy


class Status(enum.Enum):
    INITIAL = "Initial"
    RUNNING = "Running"
    SUCCESS = "Success"
    FAILURE = "Failure"
    CANCELLED = "Cancelled"
    SUSPENDED = "Suspended"
    HALTED = "Halted"

    @property
    def done(self) -> bool:
        return self in _DONE

    @property
    def live(self) -> bool:
        return self in _LIVE


_DONE = frozenset((Status.SUCCESS, Status.FAILURE, Status.CANCELLED, Status.HALTED))
_LIVE = frozenset((Status.RUNNING, Status.SUSPENDED))

# Migration aliases. TS_SUCCESS is no longer None -- see notes.
TS_INITIAL = Status.INITIAL
TS_RUNNING = Status.RUNNING
TS_SUCCESS = Status.SUCCESS
TS_FAILURE = Status.FAILURE
TS_CANCELLED = Status.CANCELLED
TS_SUSPENDED = Status.SUSPENDED
TS_HALTED = Status.HALTED


class Task(Policy):
    def __init__(self, action=None, msg=None):
        super().__init__()
        if action:
            self.use(action)
        self.msg = msg
        self.coro: Optional[Coroutine] = None

        # The task we are currently blocked on, cleared when it is resumed.
        self.awaited: Optional["Task"] = None
        # The task we were most recently blocked on, retained so a composite
        # can inspect its status after resuming.
        self.last_awaited: Optional["Task"] = None
        self.awaiter: Optional["Task"] = None

        self.result: Any = None
        self.error: Optional[BaseException] = None

        self.id = uuid1()
        self.bot: "Bot" = None
        self.runner: Optional["Runner"] = None
        self.parent: Optional["Task"] = None
        self.children: List["Task"] = []
        self.status = Status.INITIAL
        self.tasks = None

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.status.value}>"

    @classmethod
    def produce(cls, bot: "Bot", parent: "Task" = None):
        task = cls()
        return task.create(bot, parent)

    def create(self, bot: "Bot", parent: "Task" = None):
        self.bot = bot
        self.parent = parent
        if parent:
            parent.add(self)
            if self.runner is None:
                self.runner = parent.runner
        return self

    def __await__(self):
        return (yield self)

    def reset(self):
        """Return this task and its subtree to INITIAL so it can run again.

        Repeating composites (Loop, Forever, Counter) need this between
        iterations: begin() re-arms only this task's own coroutine, and
        refuses outright once status is done.
        """
        self._close()
        self.status = Status.INITIAL
        self.result = None
        self.error = None
        self.awaited = None
        self.last_awaited = None
        self.awaiter = None
        for child in self.children:
            child.reset()
        return self

    #
    # HOOKS
    #
    def enter(self):
        pass

    def exit(self, status):
        return status

    async def main(self, msg: Message = None):
        self.enter()
        return self.exit(self.succeed())

    async def sleep(self, period: float = None):
        if not period:
            # quick and dirty way to yield control back to the runner
            self.status = Status.SUSPENDED
            return await self
        return await Sleep(period)

    def ok(self) -> bool:
        return self.status is Status.RUNNING

    def use(self, fn: Coroutine):
        if not inspect.iscoroutinefunction(fn):
            raise TypeError(f"Not a coroutine function: {fn!r}")
        self.main = types.MethodType(fn, self)

    def begin(self) -> bool:
        if self.status is Status.CANCELLED:
            logger.warning("Refusing to begin a cancelled task: {}", self)
            return False
        if self.status.done:
            self.reset()
        self.coro = self.main(self.msg)
        self.status = Status.RUNNING
        return True

    '''
    def begin(self) -> bool:
        if self.status.done:
            logger.warning("Refusing to begin a finished task: {}", self)
            return False
        self.coro = self.main(self.msg)
        self.status = Status.RUNNING
        return True
    '''

    #
    # TREE
    #
    def add(self, child: "Task"):
        child.parent = self
        child.tasks = self.tasks
        if child.runner is None:
            child.runner = self.runner
        if child.bot is None:
            child.bot = self.bot
        self.children.append(child)
        return self

    def remove(self, child: "Task"):
        try:
            self.children.remove(child)
        except ValueError:
            logger.warning("Not a child of {}: {}", self, child)
        return self

    #
    # EXECUTION
    #
    def _runner(self) -> "Runner":
        return self.runner or Runner()

    def schedule_task(self, task: "Task", msg=None):
        self._runner().schedule(task, msg)

    def schedule(self, msg=None):
        self._runner().schedule(self, msg)

    def run(self, dt: float = 0.0, max_steps: int = 10000):
        return self._runner().run(self, dt=dt, max_steps=max_steps)

    def suspend(self):
        self.status = Status.SUSPENDED
        return self.status

    def resume(self):
        self.status = Status.RUNNING
        return self.status

    def succeed(self):
        return self._finish(Status.SUCCESS)

    def fail(self):
        logger.debug("fail: {}", self)
        return self._finish(Status.FAILURE)

    def halt(self):
        if self.bot:
            self.bot.halt()
        return self._finish(Status.HALTED)

    def cancel(self):
        """Cancel this task and its whole subtree.

        Not advisory: the coroutine frame is closed so it cannot be resumed,
        and the runner drops it on the next step. Anything blocked on this
        task is woken so it can observe the cancellation through
        `last_awaited.status` instead of hanging.
        """
        if self.status is Status.CANCELLED:
            return self.status
        logger.debug("cancel: {}", self)
        for child in tuple(self.children):
            child.cancel()
        return self._finish(Status.CANCELLED)

    def _finish(self, status: Status):
        """Single exit point for every terminal transition. Re-entrant safe."""
        self.status = status
        self._close()
        if self.awaited is not None:
            # We are dying while blocked; nothing will deliver our result.
            self.awaited.awaiter = None
            self.awaited = None
        awaiter = self.awaiter
        if awaiter is not None:
            self.awaiter = None
            if awaiter.status is Status.SUSPENDED:
                self._runner().reschedule(awaiter)
        return status

    def _close(self):
        """Release the suspended coroutine frame and everything it holds."""
        coro = self.coro
        if coro is None:
            return
        if inspect.getcoroutinestate(coro) == inspect.CORO_RUNNING:
            # Finishing from inside our own body. The frame unwinds on its
            # own and _advance calls _finish again on StopIteration.
            return
        self.coro = None
        try:
            coro.close()
        except Exception as e:
            logger.warning("Error closing {}: {}", self, e)

    def broadcast(self, msg: Message):
        pass

    def post(self, msg: Message):
        msg.sender = self
        return self.bot.post(msg)

    #
    # Utility
    #
    def to_json(self):
        return {
            "TYPE": self.__class__.__name__,
            "MSG": self.msg,
            "STATUS": self.status.value,
        }

    #
    # DSL
    #
    def chain(self, b):
        a = self.children[-1] if self.children else None
        if a:
            a.dst = b
            b.src = a
        self.add(b)
        return self


class Trap(Task):
    """A task the runner handles specially rather than as ordinary work."""


class NoOp(Trap):
    async def main(self, msg=None):
        return self.succeed()


class Sleep(Trap):
    """Suspend for `period` seconds of *runner* time.

    Runner time only advances when the game advances it, so pausing the game
    pauses every sleeping task, and slow motion or frame stepping need no
    special handling here.
    """

    def __init__(self, period: float):
        super().__init__()
        self.period = period
        self.start: float = 0.0

    def begin(self) -> bool:
        # Capture the start when the runner admits us, not at construction,
        # or any delay in between is eaten from the period.
        self.start = self._runner().time
        return super().begin()

    @property
    def elapsed(self) -> float:
        return self._runner().time - self.start

    async def main(self, msg=None):
        while True:
            elapsed = self.elapsed
            if elapsed >= self.period:
                return elapsed
            await self.sleep()


#
# Runner
#
@singleton
class Runner:
    """Cooperative trampoline for behaviour-tree tasks.

    Still a singleton so existing call sites keep working. Every internal
    reference goes through `task.runner`, so moving to one runner per world
    is dropping the decorator plus wiring the construction site.
    """

    def __init__(self):
        self.queue: List[Task] = []
        self.callbacks: List[Callable] = []
        self.time: float = 0.0
        self.steps: int = 0

    #
    # SCHEDULING
    #
    def trap(self, task: Trap):
        if isinstance(task, (NoOp, Sleep)):
            self._admit(task)
        else:
            raise NotImplementedError(f"No trap handler for {task!r}")

    def schedule(self, obj, msg=None):
        if inspect.iscoroutinefunction(obj):
            task = Task(obj, msg)
        elif isinstance(obj, Task):
            task = obj
            if msg is not None:
                task.msg = msg
        else:
            raise TypeError(f"Not a Task: {obj!r}")
        self._admit(task)
        return task

    def _admit(self, task: Task):
        task.runner = self
        if task.begin():
            self.queue.append(task)

    def reschedule(self, task: Task):
        if task.status.done:
            logger.debug("Refusing to reschedule finished task: {}", task)
            return
        task.status = Status.RUNNING
        self.queue.append(task)

    def cancel_all(self, max_passes: int = 100):
        """Synchronously tear everything down. Safe to call from teardown.

        Cancelling wakes awaiters, which puts them back on the queue, so this
        loops until nothing new appears. Two passes is typical: one for the
        leaves, one for the parents they wake.
        """
        self.callbacks = []
        passes = 0
        while self.queue:
            if passes >= max_passes:
                logger.error("cancel_all did not converge in {} passes", max_passes)
                self.queue = []
                break
            queue = self.queue
            self.queue = []
            for task in queue:
                if not task.status.done:
                    task.cancel()
            passes += 1

    '''
    def cancel_all(self):
        """Synchronously tear everything down. Safe to call from teardown.

        Cancelling closes coroutine frames, which is what actually releases
        their references to bots and nodes.
        """
        queue = self.queue
        self.queue = []
        for task in queue:
            if not task.status.done:
                task.cancel()
        self.callbacks = []
    '''

    #
    # STEPPING
    #
    def step(self, dt: float = 0.0):
        self.time += dt
        self.steps += 1

        queue = self.queue
        self.queue = []

        for task in queue:
            if task.status.done:
                # Cancelled or finished between being queued and being run.
                logger.debug("Dropping {}", task)
                continue
            self._advance(task)

        callbacks = self.callbacks
        self.callbacks = []
        for callback in callbacks:
            try:
                callback()
            except Exception:
                logger.error("Callback {} raised:\n{}", callback, traceback.format_exc())

    def _advance(self, task: Task):
        """Resume one task. Failures are contained to that task."""
        coro = task.coro
        if coro is None:
            logger.warning("No coroutine for {}", task)
            return

        try:
            result = None
            awaited = task.awaited
            if awaited is not None:
                result = awaited.result
                task.last_awaited = awaited
                task.awaited = None

            yielded = coro.send(result)

        except StopIteration as stop:
            value = stop.value
            if isinstance(value, Status):
                # Explicit `return self.fail()` / `return Status.X`
                final = value
            else:
                # Bare return, or a return carrying a payload.
                task.result = value
                final = task.status if task.status.done else Status.SUCCESS
            task._finish(final)
            return

        except Exception as e:
            # Previously this escaped step() and silently dropped every
            # remaining task in the batch.
            logger.error("{} raised:\n{}", task, traceback.format_exc())
            task.error = e
            task._finish(Status.FAILURE)
            return

        if yielded is task:
            # quick and dirty way to yield control back to the runner
            self.reschedule(task)
        elif yielded is not None:
            task.status = Status.SUSPENDED
            task.awaited = yielded
            yielded.awaiter = task
            if yielded.bot is None:
                yielded.bot = task.bot
            if isinstance(yielded, Trap):
                self.trap(yielded)
            else:
                self.schedule(yielded)
        else:
            logger.warning("{} yielded None; rescheduling", task)
            self.reschedule(task)

    def run(self, task: Task, dt: float = 0.0, max_steps: int = 10000):
        """Drive a task to completion. Mainly for tests and tooling.

        `dt` advances runner time per step so sleeps resolve. With dt=0 any
        task containing a Sleep spins until max_steps.
        """
        self.schedule(task)
        steps = 0
        while self.queue:
            if steps >= max_steps:
                logger.error("run() exceeded {} steps; aborting", max_steps)
                self.cancel_all()
                break
            self.step(dt)
            steps += 1
        return task.result