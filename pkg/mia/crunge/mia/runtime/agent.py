"""Agents: a context, a message queue, and tasks created from rules.

An agent runs until it halts, finishes, or reaches a decision: nothing left to
dispatch or run, with proposals waiting. `advance()` stops at that point, and
an `Agency` forks one child per proposal. `run()` commits to the first
proposal instead, which is handy for debugging a program without search.

Each agent carries `cost`, the path cost of the choices that led to it. Rules
add to it with `cost <expr>`; a commit whose rules add nothing costs 1.
"""

from __future__ import annotations

import copy
from collections import deque
from dataclasses import dataclass
from enum import Enum, auto
from functools import cache

from .clauses import Achieve, Belief, Clause, Goal, Perform
from .context import Context
from .messages import IMPASSE, Assert, Attempt, Message, Modify, Retract, Trigger
from .task import SUCCESS, Result, Status, Task
from .terms import ACTIVE, SELF, STATUS


class Step(Enum):
    DONE = auto()
    DECIDE = auto()


@dataclass(slots=True)
class Spawn:
    """A plan that runs an expert as a child agent."""

    expert: type[Agent]
    boot: Task


@dataclass(slots=True)
class Proposal:
    message: Message
    plan: Task | Spawn | None  # set when the proposal is one of several matching plans
    waiter: Task | None


class Agent:
    boot: type[Task] | None = None
    rules: tuple[type[Task], ...] = ()
    experts: tuple[type[Agent], ...] = ()
    predicates: dict = {}
    max_steps = 100_000
    priority = None  # search priority for this agent's agency; None means A*

    def __init__(self, context: Context | None = None, parent: Agent | None = None):
        self.context = context if context is not None else Context()
        self.parent = parent
        self.agents: list[Agent] = []
        self.messages: deque[tuple[object, Task | None]] = deque()
        self.ready: deque[tuple[Task, Result | None]] = deque()
        self.proposals: list[Proposal] = []
        self.suspended: list[Task] = []
        self.history: list[Message] = []
        self.steps = 0
        self.cost = 0.0
        self.step_cost = 0.0
        self.committed = False
        self.solution: Agent | None = None
        self.halted = False
        self.dead = False
        self.impassed = False

    # ------------------------------------------------------------ used by generated code

    def post(self, message, waiter: Task | None = None):
        self.messages.append((message, waiter))
        return Status.SUSPENDED if waiter is not None else None

    def propose(self, message, waiter: Task | None = None):
        self.proposals.append(Proposal(message, None, waiter))
        return Status.SUSPENDED if waiter is not None else None

    def halt(self) -> Status:
        self.halted = True
        return Status.HALTED

    def add_cost(self, amount) -> None:
        if amount < 0:
            raise ValueError(f"cost must not be negative, got {amount}")
        self.cost += amount
        self.step_cost += amount

    # ------------------------------------------------------------ running

    def run(self) -> Status:
        """Run to the end, committing to the first proposal at every decision."""
        while self.advance() is Step.DECIDE:
            self.commit(self.proposals[0])
        return self.status()

    def advance(self) -> Step:
        """Run until the agent is done or has to choose among its proposals."""
        step = self._advance()
        if self.committed and self.step_cost == 0:
            self.cost += 1
        self.committed = False
        self.step_cost = 0.0
        return step

    def _advance(self) -> Step:
        while not (self.halted or self.dead):
            if self.steps >= self.max_steps:
                self.dead = True
                break
            self.steps += 1
            if self.messages:
                self.dispatch(*self.messages.popleft())
            elif self.ready:
                self.step(*self.ready.popleft())
            elif self.proposals:
                return Step.DECIDE
            elif not self.impassed:
                self.impassed = True
                self.dispatch(IMPASSE, None)
            else:
                break
        return Step.DONE

    def status(self) -> Status:
        if self.halted:
            return Status.SUCCEEDED
        if self.dead or self.suspended:
            return Status.FAILED
        return Status.SUCCEEDED

    def fork(self, index: int) -> Agent:
        """Clone this agent and commit the clone to proposal `index`.

        One deepcopy call covers the context, queues, proposals, and suspended
        tasks, so a task waiting on a proposal is still that proposal's waiter
        in the clone. Terms, clauses, and messages are immutable and shared.
        """
        context, messages, ready, proposals, suspended = copy.deepcopy(
            (self.context, self.messages, self.ready, self.proposals, self.suspended)
        )
        child = type(self)(context, parent=self)
        child.messages, child.ready, child.proposals, child.suspended = messages, ready, proposals, suspended
        child.history = list(self.history)
        child.steps = self.steps
        child.cost = self.cost
        self.agents.append(child)
        child.commit(child.proposals[index])
        return child

    def state_key(self):
        """What makes two agents the same search state (cost excluded)."""
        return (
            frozenset(self.context),
            tuple((p.message, _plan_key(p.plan)) for p in self.proposals),
            tuple(_task_key(t) for t in self.suspended),
            self.halted,
            self.dead,
        )

    def commit(self, proposal: Proposal):
        self.proposals.clear()
        self.impassed = False
        self.committed = True
        self.step_cost = 0.0
        self.history.append(proposal.message)
        if proposal.plan is None:
            self.dispatch(proposal.message, proposal.waiter)
        else:
            self.start(proposal.plan, proposal.message, proposal.waiter)

    # ------------------------------------------------------------ dispatch

    def dispatch(self, message, waiter: Task | None):
        match message:
            case _ if message is IMPASSE:
                for plan in self.plans(message):
                    self.start(plan, message, None)
            case Assert(clause=clause):
                if self.context.add(clause):
                    self.changed(message)
            case Retract(clause=clause):
                if self.context.remove(clause):
                    self.changed(message)
            case Modify(clause=clause):
                for old in self.context.replace(clause):
                    self.changed(Retract(old))
                if self.context.add(clause):
                    self.changed(Assert(clause))
            case Attempt(clause=Achieve() as goal) if _belief(goal) in self.context:
                pass  # already achieved: succeed without running a plan
            case Attempt():
                plans = self.plans(message)
                if len(plans) == 1:
                    self.start(plans[0], message, waiter)
                elif plans:
                    # Several matching plans are alternatives, not parallel work.
                    self.proposals.extend(Proposal(message, plan, waiter) for plan in plans)
                elif waiter is not None:
                    self.ready.append((waiter, Result(False)))
                return
            case _:
                raise TypeError(f"cannot dispatch {message!r}")
        if waiter is not None:
            self.ready.append((waiter, Result(True)))

    def changed(self, event: Message):
        self.impassed = False
        self.track_goals(event)
        for plan in self.plans(event):
            self.start(plan, event, None)

    def track_goals(self, event: Message):
        """Keep `goal status Active` beliefs current.

        A perform goal is active while it's in the context. An achieve goal is
        active while it's in the context and its belief doesn't hold, so
        undoing an achieved goal makes it active again.
        """
        added = isinstance(event, Assert)
        match event.clause:
            case Achieve() as goal:
                self.set_active(goal, added and _belief(goal) not in self.context)
            case Goal() as goal:
                self.set_active(goal, added)
            case Belief() as belief:
                goal = Achieve(belief.subj, belief.verb, belief.obj, belief.slots)
                if goal in self.context:
                    self.set_active(goal, not added)

    def set_active(self, goal: Goal, active: bool):
        status = Belief(goal, STATUS, ACTIVE)
        self.post(Assert(status) if active else Retract(status))

    def plans(self, message) -> list[Task | Spawn]:
        found: list[Task | Spawn] = []
        for rule in _rules(type(self)):
            if _matches(rule.trigger, message):
                task = rule()
                if task.bind(message):
                    found.append(task)
        for expert in type(self).experts:
            if expert.boot is not None and _matches(expert.boot.trigger, message):
                task = expert.boot()
                if task.bind(message):
                    found.append(Spawn(expert, task))
        return found

    def start(self, plan: Task | Spawn, message, waiter: Task | None):
        if isinstance(plan, Spawn):
            result = self.spawn(plan, message)
            if waiter is not None:
                self.ready.append((waiter, result))
            return
        plan.message = message
        plan.waiter = waiter
        self.ready.append((plan, None))

    def step(self, task: Task, result: Result | None):
        if task in self.suspended:
            self.suspended.remove(task)
        status = task.resume(self, result)
        if status is None:
            raise RuntimeError(f"{task!r} returned no status")
        if status is Status.SUSPENDED:
            self.suspended.append(task)
            return
        if status is Status.THROWN:
            self.dead = True
        if task.waiter is not None:
            self.ready.append((task.waiter, Result(status in SUCCESS)))

    def spawn(self, plan: Spawn, message) -> Result:
        child = plan.expert(parent=self)
        self.agents.append(child)
        clause = getattr(message, "clause", None)
        source = clause.slots.get("context") if isinstance(clause, Clause) else None
        if source is not None:
            for c in source:
                child.post(Assert(c))
        child.start(plan.boot, message, None)
        from .agency import Agency

        return Result(Agency(child, plan.expert.priority).run() is not None)


class Deliberator(Agent):
    pass


class AgentHost:
    """What an application holds: creates an agent and runs its boot rule."""

    def __init__(self, agent_class: type[Agent], context: Context | None = None):
        self.agent = agent_class(context)
        self.solution: Agent | None = None

    def run(self) -> Status:
        agent = self.agent
        boot = type(agent).boot
        if boot is not None:
            trigger = boot.trigger
            message = None
            if isinstance(trigger, Trigger) and trigger.verb is not None:
                message = Attempt(Perform(SELF, trigger.verb))
            task = boot()
            if not task.bind(message):
                raise RuntimeError(f"{boot.__qualname__} did not accept its boot message")
            agent.start(task, message, None)
        from .agency import Agency

        self.solution = Agency(agent, type(agent).priority).run()
        return Status.SUCCEEDED if self.solution is not None else Status.FAILED


@cache
def _rules(cls: type[Agent]) -> tuple[type[Task], ...]:
    rules: list[type[Task]] = []
    for klass in reversed(cls.__mro__):
        for rule in vars(klass).get("rules", ()):
            if rule not in rules:
                rules.append(rule)
    return tuple(rules)


def _freeze(value):
    try:
        hash(value)
        return value
    except TypeError:
        return id(value)  # unhashable state never counts as a duplicate


def _task_key(task: Task):
    fields = sorted((k, _freeze(v)) for k, v in vars(task).items() if k.startswith(("v_", "c_")))
    return (type(task).__qualname__, task.pc, tuple(fields))


def _plan_key(plan):
    if plan is None:
        return None
    if isinstance(plan, Spawn):
        return (plan.expert.__qualname__, _task_key(plan.boot))
    return _task_key(plan)


def _belief(goal: Achieve) -> Belief:
    return Belief(goal.subj, goal.verb, goal.obj, goal.slots)


def _matches(trigger, message) -> bool:
    if trigger is IMPASSE or message is IMPASSE:
        return trigger is message
    return trigger is not None and trigger.matches(message)
