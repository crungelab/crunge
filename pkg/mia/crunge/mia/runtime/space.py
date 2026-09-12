"""Problem space: search over the states an expert could reach.

When a state has to choose among proposals, the space forks one child state
per proposal, runs each forward to its own next decision, and queues it by
priority. The first state taken off the queue that finished successfully is
the solution.

A priority is any function of a state that returns a number; lower runs
first. With `a_star()`, the priority is cost so far plus an estimate of the
cost remaining, which finds the cheapest plan as long as the estimate never
overestimates. States already reached at a lower or equal cost are dropped.
"""

from __future__ import annotations

import heapq
from collections.abc import Callable
from itertools import count

from .state import State, Step
from .clauses import Belief
from .context import ANY
from .task import Status
from .terms import ACTIVE, STATUS
from .trace import context_changes, proposals, suspended

Priority = Callable[[State], float]


def breadth_first(state: State) -> float:
    return len(state.history)


def depth_first(state: State) -> float:
    return -len(state.history)


def active_goals(state: State) -> float:
    """Default A* heuristic: the number of goals still active."""
    return len(state.context.find(Belief, ANY, STATUS, ACTIVE))


def a_star(heuristic: Callable[[State], float] = active_goals) -> Priority:
    def priority(state: State) -> float:
        return state.cost + heuristic(state)

    priority.__name__ = f"a_star({heuristic.__name__})"
    return priority


def _experts_name(state) -> str:
    """The experts active in a state, for traces: the usual case is one."""
    return " + ".join(e.__qualname__ for e in state.experts) or "State"


class ProblemSpace:
    def __init__(self, root: State, priority: Priority | None = None, max_expansions: int = 10_000):
        self.root = root
        self.priority = priority or a_star()
        self.max_expansions = max_expansions
        self.expansions = 0
        self.solution: State | None = None
        self.tracer = root.tracer
        self.id = self.tracer.next_id() if self.tracer is not None else 0
        self._frontier: list = []
        self._best: dict = {}
        self._order = count()

    def run(self) -> State | None:
        if self.tracer is not None:
            self.tracer.emit(
                "space",
                space=self.id,
                root=self.root.id,
                parent=self.root.parent.id if self.root.parent is not None else None,
                expert=_experts_name(self.root),
                priority=getattr(self.priority, "__name__", repr(self.priority)),
            )
        self._push(self.root, self.root.advance())
        while self._frontier:
            _, _, state, step, key = heapq.heappop(self._frontier)
            if self._best[key] < state.cost:
                self._emit("skip", state=state.id)
                continue
            if step is Step.DONE:
                if state.status() is Status.SUCCEEDED:
                    self.solution = self.root.solution = state
                    self._emit("solution", state=state.id, cost=state.cost)
                    break
                self._emit("dead", state=state.id)
                continue
            if self.expansions >= self.max_expansions:
                self._emit("exhausted")
                break
            self.expansions += 1
            self._emit("expand", state=state.id, expansion=self.expansions)
            for index in range(len(state.proposals)):
                child = state.fork(index)
                self._push(child, child.advance())
        self._emit(
            "result",
            solution=self.solution.id if self.solution is not None else None,
            expansions=self.expansions,
        )
        return self.solution

    def _push(self, state: State, step: Step):
        key = state.state_key()
        priority = self.priority(state)
        known = self._best.get(key)
        if self.tracer is not None:
            base = None if state is self.root else state.parent
            self._emit(
                "status",
                state=state.id,
                experts=[e.__qualname__ for e in state.experts],
                depth=len(state.history),
                step=step.name,
                status=state.status().name if step is Step.DONE else None,
                cost=state.cost,
                priority=priority,
                **context_changes(state, base),
                proposals=proposals(state),
                suspended=suspended(state),
            )
        if known is not None and known <= state.cost:
            self._emit("prune", state=state.id, best=known)
            return
        self._best[key] = state.cost
        heapq.heappush(self._frontier, (priority, next(self._order), state, step, key))

    def _emit(self, event: str, **fields):
        if self.tracer is not None:
            self.tracer.emit(event, space=self.id, **fields)
