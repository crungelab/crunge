"""Agency: search over an agent's possible futures.

When an agent has to choose among proposals, the agency forks one child per
proposal, runs each child forward to its own next decision, and queues it by
priority. The first agent taken off the queue that finished successfully is
the solution.

A priority is any function of an agent that returns a number; lower runs
first. With `a_star()`, the priority is cost so far plus an estimate of the
cost remaining, which finds the cheapest plan as long as the estimate never
overestimates. Agents whose state (context, proposals, suspended tasks) has
already been reached at a lower or equal cost are dropped.
"""

from __future__ import annotations

import heapq
from collections.abc import Callable
from itertools import count

from .agent import Agent, Step
from .clauses import Belief
from .context import ANY
from .task import Status
from .terms import ACTIVE, STATUS
from .trace import context_changes, proposals, suspended

Priority = Callable[[Agent], float]


def breadth_first(agent: Agent) -> float:
    return len(agent.history)


def depth_first(agent: Agent) -> float:
    return -len(agent.history)


def active_goals(agent: Agent) -> float:
    """Default A* heuristic: the number of goals still active."""
    return len(agent.context.find(Belief, ANY, STATUS, ACTIVE))


def a_star(heuristic: Callable[[Agent], float] = active_goals) -> Priority:
    def priority(agent: Agent) -> float:
        return agent.cost + heuristic(agent)

    priority.__name__ = f"a_star({heuristic.__name__})"
    return priority


class Agency:
    def __init__(self, root: Agent, priority: Priority | None = None, max_expansions: int = 10_000):
        self.root = root
        self.priority = priority or a_star()
        self.max_expansions = max_expansions
        self.expansions = 0
        self.solution: Agent | None = None
        self.tracer = root.tracer
        self.id = self.tracer.next_id() if self.tracer is not None else 0
        self._frontier: list = []
        self._best: dict = {}
        self._order = count()

    def run(self) -> Agent | None:
        if self.tracer is not None:
            self.tracer.emit(
                "agency",
                agency=self.id,
                root=self.root.id,
                parent=self.root.parent.id if self.root.parent is not None else None,
                agent=type(self.root).__qualname__,
                priority=getattr(self.priority, "__name__", repr(self.priority)),
            )
        self._push(self.root, self.root.advance())
        while self._frontier:
            _, _, agent, step, key = heapq.heappop(self._frontier)
            if self._best[key] < agent.cost:
                self._emit("skip", agent=agent.id)
                continue
            if step is Step.DONE:
                if agent.status() is Status.SUCCEEDED:
                    self.solution = self.root.solution = agent
                    self._emit("solution", agent=agent.id, cost=agent.cost)
                    break
                self._emit("dead", agent=agent.id)
                continue
            if self.expansions >= self.max_expansions:
                self._emit("exhausted")
                break
            self.expansions += 1
            self._emit("expand", agent=agent.id, expansion=self.expansions)
            for index in range(len(agent.proposals)):
                child = agent.fork(index)
                self._push(child, child.advance())
        self._emit(
            "result",
            solution=self.solution.id if self.solution is not None else None,
            expansions=self.expansions,
        )
        return self.solution

    def _push(self, agent: Agent, step: Step):
        key = agent.state_key()
        priority = self.priority(agent)
        known = self._best.get(key)
        if self.tracer is not None:
            base = None if agent is self.root else agent.parent
            self._emit(
                "state",
                agent=agent.id,
                depth=len(agent.history),
                step=step.name,
                status=agent.status().name if step is Step.DONE else None,
                cost=agent.cost,
                priority=priority,
                **context_changes(agent, base),
                proposals=proposals(agent),
                suspended=suspended(agent),
            )
        if known is not None and known <= agent.cost:
            self._emit("prune", agent=agent.id, best=known)
            return
        self._best[key] = agent.cost
        heapq.heappush(self._frontier, (priority, next(self._order), agent, step, key))

    def _emit(self, event: str, **fields):
        if self.tracer is not None:
            self.tracer.emit(event, agency=self.id, **fields)
