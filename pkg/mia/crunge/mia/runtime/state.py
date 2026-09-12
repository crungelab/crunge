"""States: a context, a message queue, tasks, and the experts that are active.

A state is one node of a search. It holds the working memory, the work in
flight, and the set of experts whose rules apply to it — several at once, and
they can change while it runs. A state runs until it halts, finishes, or
reaches a decision: nothing left to dispatch or run, with proposals waiting.
`advance()` stops at that point, and a `ProblemSpace` forks one child state per
proposal. `run()` commits to the first proposal instead, which is handy for
debugging a program without search.

Each state carries `cost`, the path cost of the choices that led to it. Rules
add to it with `cost <expr>`; a commit whose rules add nothing costs 1.
"""

from __future__ import annotations

import copy
from collections import deque
from collections.abc import Sequence
from dataclasses import dataclass
from enum import Enum, auto

from .clauses import Achieve, Belief, Clause, Goal
from .context import Context, View
from .expert import Expert, experts_frames, experts_rules
from .format import to_mia
from .messages import IMPASSE, START, Assert, Attempt, Message, Modify, Retract
from .task import SUCCESS, Result, Status, Task
from .terms import ACTIVE, STATUS


class Step(Enum):
    DONE = auto()
    DECIDE = auto()


@dataclass(slots=True)
class Spawn:
    """A plan that runs a nested expert in a child problem space."""

    expert: type[Expert]
    entry: Task


@dataclass(slots=True)
class Proposal:
    message: Message
    plan: Task | Spawn | None  # set when the proposal is one of several matching plans
    waiter: Task | None


class State:
    max_steps = 100_000

    def __init__(
        self,
        experts: Sequence[type[Expert]] | type[Expert] = (),
        context: Context | None = None,
        parent: State | None = None,
        tracer=None,
    ):
        if isinstance(experts, type):
            experts = (experts,)
        self.experts: tuple[type[Expert], ...] = tuple(experts)
        self.context = context if context is not None else Context()
        self._reframe()
        self.parent = parent
        self.tracer = tracer if tracer is not None else parent.tracer if parent is not None else None
        self.id = self.tracer.next_id() if self.tracer is not None else 0
        self.spawned = False
        self.states: list[State] = []
        self.messages: deque[tuple[object, Task | None]] = deque()
        self.ready: deque[tuple[Task, Result | None]] = deque()
        self.proposals: list[Proposal] = []
        self.suspended: list[Task] = []
        self.history: list[Message] = []
        self.effects: list[tuple] = []   # (function, args) recorded by `|` statements, replayed by a Plan
        self.chosen: list[str | None] = []  # the plan picked for each commit, when several matched
        self.steps = 0
        self.cost = 0.0
        self.step_cost = 0.0
        self.committed = False
        self.solution: State | None = None
        self.halted = False
        self.dead = False
        self.impassed = False

    # ------------------------------------------------------------ experts

    def _reframe(self) -> None:
        frames = experts_frames(self.experts)
        self.view = View((self.context, *frames)) if frames else self.context

    def add_expert(self, expert: type[Expert]) -> None:
        """Activate an expert's rules on this state, if they are not already."""
        if expert not in self.experts:
            self.experts += (expert,)
            self._reframe()
            self.impassed = False

    def remove_expert(self, expert: type[Expert]) -> None:
        if expert in self.experts:
            self.experts = tuple(e for e in self.experts if e is not expert)
            self._reframe()

    @property
    def predicates(self) -> dict:
        table: dict = {}
        for expert in self.experts:
            table.update(expert.predicates)
        return table

    # ------------------------------------------------------------ used by generated code

    def post(self, message, waiter: Task | None = None):
        self.messages.append((message, waiter))
        return Status.SUSPENDED if waiter is not None else None

    def propose(self, message, waiter: Task | None = None):
        self.proposals.append(Proposal(message, None, waiter))
        return Status.SUSPENDED if waiter is not None else None

    def effect(self, function, *args) -> None:
        """Record a side effect instead of performing it.

        A branch that loses the search is discarded with its effects; only the
        winning state's are replayed, in order, by its `Plan`.
        """
        self.effects.append((function, args))
        if self.tracer is not None:
            from .plan import action_text

            self.tracer.emit("action", state=self.id, text=action_text(function, args))

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
        """Run until this state is done or has to choose among its proposals."""
        step = self._advance()
        if self.halted:
            self.flush()
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

    def flush(self) -> None:
        """Apply queued context changes without firing triggers.

        Halting stops the state mid-queue, but facts a rule asserted before it
        halted belong in the final state.
        """
        while self.messages:
            message, _ = self.messages.popleft()
            match message:
                case Assert(clause=clause):
                    self.context.add(clause)
                case Retract(clause=clause):
                    self.context.remove(clause)
                case Modify(clause=clause):
                    self.context.replace(clause)
                    self.context.add(clause)

    def status(self) -> Status:
        if self.halted:
            return Status.SUCCEEDED
        if self.dead or self.suspended:
            return Status.FAILED
        return Status.SUCCEEDED

    def fork(self, index: int) -> State:
        """Clone this state and commit the clone to proposal `index`.

        One deepcopy call covers the context, queues, proposals, and suspended
        tasks, so a task waiting on a proposal is still that proposal's waiter
        in the clone. Terms, clauses, and messages are immutable and shared.
        """
        context, messages, ready, proposals, suspended = copy.deepcopy(
            (self.context, self.messages, self.ready, self.proposals, self.suspended)
        )
        child = State(self.experts, context, parent=self)
        child.messages, child.ready, child.proposals, child.suspended = messages, ready, proposals, suspended
        child.history = list(self.history)
        child.chosen = list(self.chosen)
        child.effects = list(self.effects)
        child.steps = self.steps
        child.cost = self.cost
        self.states.append(child)
        proposal = child.proposals[index]
        if self.tracer is not None:
            self.tracer.emit(
                "fork",
                state=child.id,
                parent=self.id,
                proposal=to_mia(proposal.message),
                plan=_plan_name(proposal.plan),
            )
        child.commit(proposal)
        return child

    def state_key(self):
        """What makes two states the same for the search (cost excluded)."""
        return (
            frozenset(self.context),
            tuple((p.message, _plan_key(p.plan)) for p in self.proposals),
            tuple(_task_key(t) for t in self.suspended),
            self.experts,
            self.halted,
            self.dead,
        )

    def commit(self, proposal: Proposal):
        self.proposals.clear()
        self.impassed = False
        self.committed = True
        self.step_cost = 0.0
        self.history.append(proposal.message)
        self.chosen.append(_plan_name(proposal.plan))
        if proposal.plan is None:
            self.dispatch(proposal.message, proposal.waiter)
        else:
            self.start(proposal.plan, proposal.message, proposal.waiter)

    # ------------------------------------------------------------ dispatch

    def dispatch(self, message, waiter: Task | None):
        match message:
            case _ if message is IMPASSE or message is START:
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
        for rule in experts_rules(self.experts):
            if _matches(rule.trigger, message):
                task = rule()
                if task.bind(message):
                    found.append(task)
        for expert in self.sub_experts():
            if expert.entry is not None and _matches(expert.entry.trigger, message):
                task = expert.entry()
                if task.bind(message):
                    found.append(Spawn(expert, task))
        return found

    def sub_experts(self) -> tuple[type[Expert], ...]:
        """Experts nested inside the active ones, which their messages can spawn."""
        return tuple(nested for expert in self.experts for nested in expert.experts)

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
        if task.waiter is not None:
            if status is Status.THROWN:
                self.dead = True
            self.ready.append((task.waiter, Result(status in SUCCESS)))
        elif status not in SUCCESS:
            # Nobody is waiting on this task, so its failure ends the branch.
            self.dead = True

    def spawn(self, plan: Spawn, message) -> Result:
        child = State(plan.expert, parent=self)
        child.spawned = True
        self.states.append(child)
        if self.tracer is not None:
            self.tracer.emit(
                "spawn", state=child.id, parent=self.id, expert=plan.expert.__qualname__, message=to_mia(message)
            )
        clause = getattr(message, "clause", None)
        source = clause.slots.get("context") if isinstance(clause, Clause) else None
        if source is not None:
            for c in source:
                child.post(Assert(c))
        child.start(plan.entry, message, None)
        from .space import ProblemSpace

        solution = ProblemSpace(child, plan.expert.priority).run()
        if solution is not None:
            # The sub-space's chosen branch is part of this state's plan.
            self.effects.extend(solution.effects)
        return Result(solution is not None)


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
        return (plan.expert.__qualname__, _task_key(plan.entry))
    return _task_key(plan)


def _plan_name(plan) -> str | None:
    if plan is None:
        return None
    if isinstance(plan, Spawn):
        return plan.expert.__name__
    return type(plan).__name__


def _belief(goal: Achieve) -> Belief:
    return Belief(goal.subj, goal.verb, goal.obj, goal.slots)


_SIGNALS = (IMPASSE, START)


def _matches(trigger, message) -> bool:
    if trigger in _SIGNALS or message in _SIGNALS:
        return trigger is message
    return trigger is not None and trigger.matches(message)
