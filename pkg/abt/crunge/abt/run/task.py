from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, List, Optional, Coroutine

if TYPE_CHECKING:
    from .agent import Agent

import enum
import types
import inspect
import traceback
from uuid import uuid1

from loguru import logger

from crunge.core.base_node import BaseNode

from ..utils import singleton
from ..run.message import Message
from .scope import TaskScope, AgentScope
from .rule_kit import Rule, RuleKit


class Status(enum.Enum):
    INITIAL = "Initial"
    RUNNING = "Running"
    SUCCESS = "Success"
    FAILURE = "Failure"
    CANCELLED = "Cancelled"
    SUSPENDED = "Suspended"
    HALTED = "Halted"
    ABORTED = "Aborted"

    @property
    def done(self) -> bool:
        return self in _DONE

    @property
    def live(self) -> bool:
        return self in _LIVE


_DONE = frozenset(
    (
        Status.SUCCESS,
        Status.FAILURE,
        Status.CANCELLED,
        Status.HALTED,
        Status.ABORTED,
    )
)
_LIVE = frozenset((Status.RUNNING, Status.SUSPENDED))


class Preempt(BaseException):
    """Unwind the running branch back to `target`, which will re-select.

    BaseException so a stray `except Exception:` inside an action body cannot
    swallow it. The runner walks the awaiter chain throwing this upward; every
    task it passes through finishes ABORTED, and the first one that catches it
    -- normally the Utility named as `target` -- absorbs it and picks again.
    """

    def __init__(self, target: Optional["Task[Any]"] = None):
        self.target = target
        super().__init__(target)


class Task[T: Task](BaseNode[T]):
    """A node in a behaviour tree.

    Two state machines share this object and stay separate on purpose.
    `Status` is the run of a single attempt -- RUNNING, SUCCESS, ABORTED --
    and turns over many times across a task's life. Lifetime, inherited from
    Base, is the existence of the object: created once, destroyed once. A
    task that fails is not disabled, and a task that is disabled has not
    failed.

    They meet at exactly two points. `Runner._admit` drives `create()`, so a
    task's chips exist by the time its body first runs; `_destroy` cancels a
    still-live status, so tearing down a subtree cannot leave a coroutine
    frame suspended forever.

    The tree comes from BaseNode. `add_child` sets the link, fires the hooks,
    and syncs lifetime; `on_child_added` is where the ambient scope --
    runner, agent, task list -- is backfilled onto a child that was built
    without one.
    """

    # Cleared for the span of an action that must not be torn down mid-flight
    # (an Eat that has already committed, say). Deferral, not veto: the check
    # simply runs again next step.
    interruptible: bool = True

    def __init__(self, action=None, msg=None):
        super().__init__()
        if action:
            self.use(action)
        self.msg = msg
        self.coro: Optional[Coroutine] = None

        # The task we are currently blocked on, cleared when it is resumed.
        self.awaited: Optional[Task[Any]] = None
        # The task we were most recently blocked on, retained so a composite
        # can inspect its status after resuming.
        self.last_awaited: Optional[Task[Any]] = None
        self.awaiter: Optional[Task[Any]] = None

        self.result: Any = None
        self.error: Optional[BaseException] = None

        self.id = uuid1()
        self.status = Status.INITIAL

        # Ambient scope. Both are None outside any open `with`, which is the
        # normal case for tasks built at run time; on_child_added backfills
        # from the parent when such a task is later attached to a live tree.
        self.runner: Optional[Runner] = None

        self.agent: Optional["Agent"] = AgentScope.top()

        self._rules: Optional[RuleKit] = None
        '''
        # `parent` and `children` belong to BaseNode now; attachment is what
        # sets the link, not assignment.
        parent = TaskScope.top()
        if parent is not None:
            parent.add_child(self)
            # Scope wins over ambient for a task built inside a `with`: the
            # is-None guards in on_child_added are for the runtime path.
            self.agent = parent.agent
            self.runner = parent.runner
        '''

    def __enter__(self) -> "Task[T]":
        # `parent` and `children` belong to BaseNode now; attachment is what
        # sets the link, not assignment.
        parent = TaskScope.top()
        if parent is not None:
            parent.add_child(self)

        TaskScope.push(self)
        return self

    def __exit__(self, exc_type, exc_value, tb):
        TaskScope.pop(self)
        return False

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.status.value}>"

    def __await__(self):
        return (yield self)

    def reset(self):
        """Return this task and its subtree to INITIAL so it can run again.

        Repeating composites (Loop, Forever, Counter) need this between
        iterations: begin() re-arms only this task's own coroutine, and
        refuses outright once status is done.

        Status only. Lifetime is untouched -- a reset task keeps its chips
        and stays created.
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

    #
    # PREEMPTION
    #
    def check(self) -> Optional["Task[Any]"]:
        """Ask whether the branch we are on should be torn down right now.

        Returns the task that should absorb the Preempt and re-select, or None
        to carry on. The runner calls this on the task it is about to resume,
        which is always the live leaf -- suspended composites are not queued.

        The default walks up and asks the same question of whoever is above,
        so an arbiter anywhere on the path can answer. A Utility overrides it
        to compare its incumbent against its siblings, asking upward *first*
        so the shallowest changed decision wins:

            def check(self):
                victim = super().check()
                if victim is not None:
                    return victim
                if self.current is None:
                    return None
                if self.best_child() is not self.current:
                    return self
                return None

        `parent` is the static tree link, but tasks built at run time (a Sleep
        awaited from inside a body) have no parent, so fall back to the awaiter
        chain -- otherwise a branch would be un-preemptible for as long as it
        happened to be sleeping.
        """
        up = self.parent if self.parent is not None else self.awaiter
        if up is not None:
            return up.check()
        return None

    #
    # TREE
    #
    # add_child / remove_child / children / parent come from BaseNode. This
    # hook is the old add()'s backfill: a task built at run time carries no
    # ambient scope, so it inherits ours on attachment.
    #
    def on_child_added(self, child: T) -> None:
        if child.runner is None:
            child.runner = self.runner
        if child.agent is None:
            child.agent = self.agent

    #
    # RULES
    #
    # Declared rules live on the class, shared by every instance. A task
    # that gains one at run time forks into a kit of its own, so a
    # subscription cannot leak into its siblings.
    #
    def add_rule(self, rule: Rule) -> Rule:
        kit = self._rules
        if kit is None:
            inherited = self.get_cls_chip(RuleKit)
            kit = self._rules = (
                inherited.fork(self) if inherited is not None else RuleKit(owner=self)
            )
        return kit.add_rule(rule)

    def match_rules(self, msg: Message):
        kit = self._rules or self.get_cls_chip(RuleKit)
        if kit is None:
            return ()
        return kit.match(msg)

    #
    # EXECUTION
    #
    def _runner(self) -> "Runner":
        return self.runner or Runner()

    def schedule_task(self, task: "Task[Any]", msg=None):
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
        if self.agent:
            self.agent.halt()
        return self._finish(Status.HALTED)

    def abort(self):
        """Terminal, but distinct from failure: the branch was displaced.

        A composite that sees ABORTED on last_awaited should unwind rather
        than run its failure recovery -- nothing went wrong, something else
        simply outranked it.
        """
        return self._finish(Status.ABORTED)

    def cancel(self):
        """Cancel this task and its whole subtree.

        Not advisory: the coroutine frame is closed so it cannot be resumed,
        and the runner drops it on the next step. Anything blocked on this
        task is woken so it can observe the cancellation through
        `last_awaited.status` instead of hanging.

        Status only -- a cancelled task is still created and still holds its
        chips. Destroying is a separate act.
        """
        if self.status is Status.CANCELLED:
            return self.status
        logger.debug("cancel: {}", self)
        for child in tuple(self.children):
            child.cancel()
        return self._finish(Status.CANCELLED)

    def _finish(self, status: Status, wake: bool = True):
        """Single exit point for every terminal transition. Re-entrant safe.

        `wake=False` is for the preempt walk: the awaiter is about to be
        thrown into by the runner, so rescheduling it here would queue a task
        that is already being resumed.
        """
        self.status = status
        self._close()
        if self.awaited is not None:
            # We are dying while blocked; nothing will deliver our result.
            self.awaited.awaiter = None
            self.awaited = None
        awaiter = self.awaiter
        if awaiter is not None:
            self.awaiter = None
            if wake and awaiter.status is Status.SUSPENDED:
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

    #
    # LIFETIME
    #
    def _destroy(self) -> None:
        """Close the status machine before the object goes away.

        destroy_children runs ahead of this, so each child has already
        cancelled itself on the way down -- no need to recurse through
        cancel() and walk the tree a second time. wake=False because the
        awaiter is being torn down in the same pass.
        """
        if not self.status.done:
            self._finish(Status.CANCELLED, wake=False)
        super()._destroy()

    #
    # Messaging
    #
    def dispatch(self, msg: Message) -> bool:
        for child in self.children:
            if child.dispatch(msg):
                return True

        # Previously fell off the end returning None, so a fired rule never
        # stopped propagation and every sibling saw the message anyway.
        fired = False
        for match in self.match_rules(msg):
            logger.debug("Fire:\t{}:", match)
            self.schedule_task(match.rule.action, match.msg)
            fired = True
        if fired:
            return True
        return super().dispatch(msg)

    '''
    def broadcast(self, msg: Message):
        pass
    '''

    def subscribe(self, trigger, action) -> Rule:
        return self.add_rule(Rule(trigger, action))

    def unsubscribe(self, rule: Rule) -> None:
        if self._rules is not None:
            self._rules.remove_rule(rule)

    def post(self, msg: Message) -> None:
        self.agent.post(msg)

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
        self.add_child(b)
        return self


class Trap(Task["Trap"]):
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
        self.queue: List[Task[Any]] = []
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

    def _admit(self, task: Task[Any]):
        task.runner = self
        # The one place status and lifetime meet on the way in. Both are
        # idempotent, so re-admitting a task is free; the first admission is
        # what seats and creates its chips, and create_children carries that
        # down the subtree.
        #task.create()
        #task.enable()
        if task.begin():
            self.queue.append(task)

    def reschedule(self, task: Task[Any]):
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
                logger.error(
                    "Callback {} raised:\n{}", callback, traceback.format_exc()
                )

    def _advance(self, task: Task[Any]):
        """Resume one task. Failures are contained to that task."""
        coro = task.coro
        if coro is None:
            logger.warning("No coroutine for {}", task)
            return

        # Arbitration happens before the body runs, not after: an act whose
        # branch has been outranked should not get one more frame of effect.
        victim = task.check() if task.interruptible else None
        if victim is not None:
            logger.debug("preempt: {} -> {}", task, victim)
            self._preempt(task, victim)
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

        except Preempt:
            # Raised from inside a body rather than thrown in by us. Nothing
            # below is holding it, so it dies here instead of escaping step().
            logger.warning("{} raised Preempt outside the preempt walk", task)
            task._finish(Status.ABORTED)
            return

        except Exception as e:
            # Previously this escaped step() and silently dropped every
            # remaining task in the batch.
            logger.error("{} raised:\n{}", task, traceback.format_exc())
            task.error = e
            task._finish(Status.FAILURE)
            return

        self._dispatch(task, yielded)

    def _preempt(self, task: Task[Any], victim: Task[Any]):
        """Unwind the awaiter chain until `victim` absorbs the Preempt.

        Each task in this runner owns its own coroutine, so frames along the
        path are siblings rather than nested -- a raise in the leaf does not
        propagate to its composite on its own. We walk it by hand. Throwing
        into an awaiter resumes it at the `yield self` inside its child's
        __await__, which is where per-act abort handling lives.
        """
        exc = Preempt(victim)

        while task is not None:
            awaiter = task.awaiter
            coro = task.coro

            # The child we were blocked on is dead or dying. Drop the link now
            # or a resumed composite reads a stale result off it.
            if task.awaited is not None:
                task.last_awaited = task.awaited
                task.awaited.awaiter = None
                task.awaited = None

            if coro is None:
                logger.warning("No coroutine to preempt for {}", task)
                task._finish(Status.ABORTED, wake=False)
                task = awaiter
                continue

            try:
                yielded = coro.throw(exc)

            except Preempt as raised:
                if raised is not exc:
                    logger.warning("{} substituted its own Preempt", task)
                # Did not absorb it. Abort and carry it upward. wake=False:
                # the awaiter is next in this walk, not queue material.
                task._finish(Status.ABORTED, wake=False)
                task = awaiter
                continue

            except StopIteration as stop:
                # Absorbed and ran to completion in the same breath.
                value = stop.value
                if isinstance(value, Status):
                    final = value
                else:
                    task.result = value
                    final = task.status if task.status.done else Status.SUCCESS
                task._finish(final)
                return

            except Exception as e:
                logger.error(
                    "{} raised while preempting:\n{}", task, traceback.format_exc()
                )
                task.error = e
                task._finish(Status.FAILURE)
                return

            # Absorbed: it re-selected and handed us whatever it wants next.
            self._dispatch(task, yielded)
            return

        logger.error(
            "Preempt targeting {} escaped the root; branch is now dead", victim
        )

    def _dispatch(self, task: Task[Any], yielded):
        """Route whatever a resumed task handed back."""
        if yielded is task:
            self.reschedule(task)
        elif yielded is not None:
            task.status = Status.SUSPENDED
            task.awaited = yielded
            if yielded.agent is None:
                yielded.agent = task.agent

            if isinstance(yielded, Trap):
                self.trap(yielded)
            else:
                self.schedule(yielded)

            # After admission, never before: awaiting a finished task sends
            # begin() through reset(), which clears awaiter. Re-selection is
            # the only path that awaits a done task, so this stayed hidden.
            if yielded.status.done:
                logger.warning("{} refused admission for {}", yielded, task)
                task.awaited = None
                self.reschedule(task)
                return
            yielded.awaiter = task
        else:
            logger.warning("{} yielded None; rescheduling", task)
            self.reschedule(task)

    def run(self, task: Task[Any], dt: float = 0.0, max_steps: int = 10000):
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