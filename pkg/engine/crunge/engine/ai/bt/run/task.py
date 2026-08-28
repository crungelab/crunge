from typing import TYPE_CHECKING, Any, Callable, List, Optional, Union, Coroutine

if TYPE_CHECKING:
    from .bot import Bot

import types
import time
from uuid import uuid1
import inspect

from loguru import logger

from ..utils import singleton
from ..run import Message
from .policy import Policy

TS_INITIAL = "Initial"
TS_RUNNING = "Running"
TS_SUCCESS = None
TS_FAILURE = "Failure"
TS_CANCELLED = "Cancelled"
TS_SUSPENDED = "Suspended"
TS_HALTED = "Halted"


class Task(Policy):
    def __init__(self, action=None, msg=None):
        super().__init__()
        if action:
            self.use(action)
        self.msg = msg
        self.coro: Coroutine = None
        self.awaited = None
        self.awaiter = None
        self.result: Any = None

        self.id = uuid1()
        self.bot: "Bot" = None
        self.parent: Task = None
        self.children: List[Task] = []
        self.status = TS_INITIAL
        self.tasks = None

    @classmethod
    def produce(cls, bot: "Bot", parent: "Task" = None):
        task = cls()
        return task.create(bot, parent)

    def create(self, bot: "Bot", parent: "Task" = None):
        self.bot = bot
        self.parent = parent
        if parent:
            parent.add(self)
        return self

    def __await__(self):
        return (yield self)

    def enter(self):
        pass

    def exit(self, status):
        return status

    async def main(self, msg: Message = None):
        self.enter()
        self.exit(self.succeed())

    async def sleep(self, period: float = None):
        # logger.debug(f'sleep: {period}')
        if not period or period == 0:
            # quick and dirty way to yield control back to the runner
            self.status = TS_SUSPENDED
            return await self
        return await Sleep(period)

    def ok(self):
        if self.status == TS_RUNNING:
            return True
        return False

    def use(self, fn: Coroutine):
        if not inspect.iscoroutinefunction(fn):
            raise Exception("Not a coroutine!", fn)
        # self.main = Method(self, fn)
        self.main = types.MethodType(fn, self)

    def begin(self):
        self.coro: Coroutine = self.main(self.msg)
        self.status = TS_RUNNING
        return True

    def add(self, child: "Task"):
        child.parent = self
        child.tasks = self.tasks
        self.children.append(child)
        return self

    def remove(self, child: "Task"):
        try:
            self.children.remove(child)
        except ValueError as e:
            print(e)
            exit()
        return self

    #
    # EXECUTION
    #
    def schedule_task(self, task: "Task", msg=None):
        Runner().schedule(task, msg)

    def schedule(self, msg=None):
        Runner().schedule(self, msg)

    def run(self):
        Runner().run(self)

    def suspend(self):
        self.status = TS_SUSPENDED
        return self.status

    def resume(self):
        self.status = TS_RUNNING
        return self.status

    def succeed(self):
        self.status = TS_SUCCESS
        return self.status

    def fail(self):
        logger.debug(f"fail: {self}")
        self.status = TS_FAILURE
        return self.status

    def cancel(self):
        logger.debug(f"cancel: {self}")
        self.status = TS_CANCELLED
        for child in self.children:
            child.cancel()

    def halt(self):
        if self.bot:
            self.bot.halt()
        self.status = TS_HALTED
        return self.status

    def broadcast(self, msg: Message):
        pass

    def post(self, msg: Message):
        msg.sender = self
        return self.bot.post(msg)

    #
    # Utility
    #
    def to_json(self):
        return {"TYPE": self.__class__.__name__, "MSG": self.msg}

    #
    # DSL
    #
    def chain(self, b):
        a = self.children[-1]
        if a:
            a.dst = b
            b.src = a
        self.add(b)
        return self


class Trap(Task):
    pass


class NoOp(Trap):
    pass


NOOP = NoOp()


class Sleep(Trap):
    def __init__(self, period: float):
        super().__init__()
        self.period = period
        self.start = time.time()

    async def main(self, msg=None):
        while True:
            current = time.time()
            elapsed = current - self.start
            logger.debug(f"elapsed {elapsed}")
            logger.debug(f"period {self.period}")
            if elapsed >= self.period:
                logger.debug("wake up")
                return elapsed
            logger.debug("sleep some more")
            await self.sleep()


#
# Runner
#
@singleton
class Runner:
    def __init__(self):
        self.queue: List[Task] = []
        self.callbacks: List[Callable] = []

    def trap(self, task):
        if isinstance(task, NoOp):
            self.schedule(task)
        elif isinstance(task, Sleep):
            # run it as a normal task
            self.schedule(task)
        else:
            raise Exception("Not implemented")

    def schedule(self, obj, msg=None):
        logger.debug(f"schedule msg {msg}")
        task = None
        if inspect.iscoroutinefunction(obj):
            task = Task(obj, msg)
        elif not isinstance(obj, Task):
            raise Exception("Not a Task!", obj)
        else:
            task = obj
        ready = task.begin()
        if ready:
            self.queue.append(task)

    def reschedule(self, task: Task):
        task.status = TS_RUNNING
        self.queue.append(task)

    def step(self):
        logger.debug("Runner.step")
        queue = self.queue
        self.queue: List[Task] = []
        for task in queue:
            logger.debug(f"task {task}")
            logger.debug(f"task.status {task.status}")
            try:
                logger.debug(f"task.coro {task.coro}")
                result = None
                if task.awaited:
                    result = task.awaited.result
                    task.awaited = None

                awaited = task.coro.send(result)
                logger.debug(f"awaited: {awaited}")

                if awaited is task:
                    # quick and dirty way to yield control back to the runner
                    logger.debug("task yielded control")
                    self.reschedule(task)
                elif awaited:
                    task.status = TS_SUSPENDED
                    task.awaited = awaited
                    awaited.awaiter = task
                    # self.schedule(awaited)
                    if isinstance(awaited, Trap):
                        self.trap(awaited)
                    else:
                        self.schedule(awaited)

            except StopIteration as exception:
                result = exception.value
                logger.debug(f"stop result {result}")
                task.result = result
                if task.awaiter:
                    logger.debug(f"task.awaiter {task.awaiter}")
                    self.reschedule(task.awaiter)

            # except Failure as exception:

        callbacks = self.callbacks
        self.callbacks = []
        for callback in callbacks:
            callback()

    def run(self, task):
        logger.debug("Runner.run")
        self.schedule(task)
        while len(self.queue) != 0:
            self.step()
