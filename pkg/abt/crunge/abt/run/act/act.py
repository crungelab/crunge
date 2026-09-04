from typing import List

from loguru import logger

from ..task import Task, Status, TS_SUCCESS, TS_FAILURE
from ..policy import Rule
from .. import Message, Propose, Attempt, Assert, Retract, Achieve
from .neuron import Neuron
from .helpers import *


class Act(Task):
    def __init__(self, action=None, msg=None):
        super().__init__(action, msg)
        self.neuron: Neuron = None

    @property
    def activity(self):
        if self.neuron:
            return self.neuron.activity
        return 1

    def activate(self):
        if self.neuron:
            return self.neuron.activate()

    def deactivate(self):
        if self.neuron:
            return self.neuron.deactivate()

    def __await__(self):
        activity = self.activity
        if activity > 0:
            return (yield self)
        # Never ran, so nothing set our status. Do it here or an awaiting
        # composite reads a stale INITIAL off last_awaited.
        self.status = Status.FAILURE
        return None

    #
    # CHILD STATUS
    #
    def child_status(self) -> Status:
        """Status of the child we most recently awaited.

        `await child` evaluates to the child's *return value* now, so
        composites branch on this instead. A child that was cancelled, failed,
        or raised is no longer indistinguishable from one that succeeded.

        Call this before resetting the child -- reset clears its status.
        """
        awaited = self.last_awaited
        return awaited.status if awaited is not None else Status.FAILURE

    def child_ok(self) -> bool:
        return self.child_status() is Status.SUCCESS

    def define(self, trigger, action):
        return self.add_rule(Rule(trigger, action))

    # Legacy. remove after fixing parser
    def sig(self, trigger, action):
        return self.define(trigger, action)

    def propose(self, c) -> None:
        self.post(Propose(c, self))

    def attempt(self, c) -> None:
        self.post(Attempt(c, self))

    def declare(self, c) -> None:
        self.post(Assert(c, self))

    def retract(self, c) -> None:
        self.post(Retract(c, self))

    def perform(self, s, p, o, x) -> None:
        c = Achieve(s, p, o, x)
        m = Attempt(c, self)
        self.post(m)

    def call(self, s, p, o, x) -> Status:
        c = Achieve(s, p, o, x)
        m = Attempt(c, self)
        self.post(m)
        return self.suspend()


#
# Root
#
@contextmanager
def root(agent):
    agent_ctx_root.set(agent)
    ctx = task_ctx_enter(agent)
    yield agent
    task_ctx_exit(ctx)


#
# Sensor
#
class Sensor(Act):
    pass


@contextmanager
def sensor():
    task = Sensor()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


sensor_ = lambda: Sensor()


#
# Condition
#
class Condition(Act):
    async def main(self, msg=None):
        for child in self.children:
            await child
            if not self.child_ok():
                return self.fail()


@contextmanager
def condition(task=None):
    if not task:
        task = Condition()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


condition_ = lambda: Condition()


#
# Action
#
class Action(Act):
    pass


@contextmanager
def action(task=None):
    if not task:
        task = Action()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


action_ = lambda action: Action(action)


#
# Sequence
#
class Sequence(Act):
    async def main(self, msg=None):
        for child in self.children:
            await child
            if not self.child_ok():
                return self.fail()


@contextmanager
def sequence(task=None):
    if not task:
        task = Sequence()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Selector
#
class Selector(Act):
    async def main(self, msg=None):
        for child in self.children:
            await child
            status = self.child_status()
            logger.debug("selector child: {} -> {}", child, status)
            if status is Status.SUCCESS:
                return
            if status is Status.CANCELLED:
                # Torn down, not a failed alternative. Don't try the rest.
                return self.cancel()
        return self.fail()


@contextmanager
def selector():
    task = Selector()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Utility
#
class Utility(Act):
    def enter(self):
        for child in self.children:
            child.activate()

    def exit(self, status=None):
        for child in self.children:
            child.deactivate()
        return status

    async def main(self, msg=None):
        self.enter()
        try:
            highest = 0
            best = None
            for child in self.children:
                activity = child.activity
                if activity > highest:
                    highest = activity
                    best = child
            logger.debug("utility best: {}", best)
            if best is None:
                return self.fail()
            await best
            if not self.child_ok():
                return self.fail()
        finally:
            self.exit()


@contextmanager
def utility():
    task = Utility()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Timer
#
class Timer(Act):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    async def main(self, msg=None):
        deadline = self._runner().time + self.timeout
        for child in self.children:
            if self._runner().time >= deadline:
                return self.fail()
            await child
            if not self.child_ok():
                return self.fail()


@contextmanager
def timer(timeout):
    task = Timer(timeout)
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Loop
#
class Loop(Act):
    def __init__(self):
        super().__init__()

    async def main(self, msg: Message = None):
        while self.ok():
            for child in self.children:
                await child
                if not self.child_ok():
                    return self.fail()
                # Recursive reset -- begin() alone only re-arms this child's
                # own coroutine and leaves its subtree finished.
                child.reset()


@contextmanager
def loop():
    task = Loop()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Forever
#
class Forever(Act):
    def __init__(self):
        super().__init__()

    async def main(self, msg=None):
        while self.ok():
            for child in self.children:
                await child
                status = self.child_status()
                logger.debug("forever child: {} -> {}", child, status)
                if status is Status.CANCELLED:
                    return self.cancel()
                # Failure is ignored here by design; restart the child.
                child.reset()


@contextmanager
def forever():
    task = Forever()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Counter
#
class Counter(Act):
    def __init__(self, start, stop):
        super().__init__()
        self.count_start = start
        self.count_stop = stop
        self.count = 0

    async def main(self, msg=None):
        for i in range(self.count_start, self.count_stop):
            self.count = i
            for child in self.children:
                await child
                if not self.child_ok():
                    return self.fail()
                child.reset()


@contextmanager
def counter(start, stop):
    task = Counter(start, stop)
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Parallel
#
class Parallel(Act):
    def __init__(self):
        super().__init__()

    async def main(self, msg=None):
        for child in self.children:
            self.schedule_task(child)
        return self.suspend()


@contextmanager
def parallel():
    task = Parallel()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Method
#
class Method(Sequence):
    pass


method_ = lambda action: Method(action)


#
# Module
#
class Module(Method):
    pass


module_ = lambda action: Module(action)

sequence_ = lambda action: Sequence(action)

counter_ = lambda start, stop, action: Counter(start, stop, action)

parallel_ = lambda action: Parallel(action)