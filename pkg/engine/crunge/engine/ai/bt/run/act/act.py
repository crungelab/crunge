from typing import List

from loguru import logger

from ..task import Task, TS_SUCCESS, TS_FAILURE
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
        return TS_FAILURE

    def define(self, trigger, action):
        return self.add_rule(Rule(trigger, action))

    def sig(self, trigger, action):
        # self.bot.signal(trigger, self)
        return self.define(trigger, action)

    def propose(self, c):
        return self.post(Propose(c, self))

    def attempt(self, c):
        return self.post(Attempt(c, self))

    def declare(self, c):
        return self.post(Assert(c, self))

    def retract(self, c):
        return self.post(Retract(c, self))

    def perform(self, s, p, o, x):
        c = Achieve(s, p, o, x)
        m = Attempt(c, self)
        return self.post(m)

    def call(self, s, p, o, x):
        c = Achieve(s, p, o, x)
        m = Attempt(c, self)
        self.post(m)
        return self.suspend()


#
# Root
#
@contextmanager
def root(bot):
    bot_ctx_root.set(bot)
    ctx = task_ctx_enter(bot)
    yield bot
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
            result = await child
            if result is TS_FAILURE:
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
            result = await child
            if result is TS_FAILURE:
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
            logger.debug(f"selector await child: {child}")
            result = await child
            logger.debug(f"selector result: {result}")
            if result is TS_SUCCESS:
                break
        else:
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

    def exit(self):
        for child in self.children:
            child.deactivate()

    async def main(self, msg=None):
        highest = 0
        best = None
        for child in self.children:
            activity = child.activity
            if activity > highest:
                highest = activity
                best = child
        logger.debug(f"utility best: {best}")
        if best is not None:
            result = await best
            logger.debug(f"utility result: {result}")


@contextmanager
def utility():
    task = Utility()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Loop
#
class Timer(Act):
    def __init__(self, timeout):
        super().__init__()
        self.timeout = timeout

    async def main(self, msg=None):
        for child in self.children:
            try:
                await child
            except Failure:
                return


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
                result = await child
                logger.debug(f"loop result: {result}")
                if result is TS_FAILURE:
                    return self.fail()


@contextmanager
def loop():
    task = Loop()
    ctx = task_ctx_enter(task)
    yield task
    task_ctx_exit(ctx)


#
# Loop
#
class Forever(Act):
    def __init__(self):
        super().__init__()

    async def main(self, msg=None):
        while self.ok():
            for child in self.children:
                result = await child
                logger.debug(f"forever result: {result}")


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
                result = await child
                logger.debug(f"counter result: {result}")
                if result is TS_FAILURE:
                    return self.fail()


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
