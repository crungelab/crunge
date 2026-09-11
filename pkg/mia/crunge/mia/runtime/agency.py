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

    return priority


class Agency:
    def __init__(self, root: Agent, priority: Priority | None = None, max_expansions: int = 10_000):
        self.root = root
        self.priority = priority or a_star()
        self.max_expansions = max_expansions
        self.expansions = 0
        self.solution: Agent | None = None
        self._frontier: list = []
        self._best: dict = {}
        self._order = count()

    def run(self) -> Agent | None:
        self._push(self.root, self.root.advance())
        while self._frontier:
            _, _, agent, step, key = heapq.heappop(self._frontier)
            if self._best[key] < agent.cost:
                continue  # a cheaper path to the same state was found later
            if step is Step.DONE:
                if agent.status() is Status.SUCCEEDED:
                    self.solution = self.root.solution = agent
                    return agent
                continue
            if self.expansions >= self.max_expansions:
                break
            self.expansions += 1
            for index in range(len(agent.proposals)):
                child = agent.fork(index)
                self._push(child, child.advance())
        return None

    def _push(self, agent: Agent, step: Step):
        key = agent.state_key()
        known = self._best.get(key)
        if known is not None and known <= agent.cost:
            return
        self._best[key] = agent.cost
        heapq.heappush(self._frontier, (self.priority(agent), next(self._order), agent, step, key))
