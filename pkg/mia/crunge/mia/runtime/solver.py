"""ProblemSolver: the entry point an application holds."""

from __future__ import annotations

from .context import Context
from .expert import Expert
from .messages import START, Assert
from .state import State
from .task import Status


class ProblemSolver:
    """Seeds the first state with a program's world and searches from it."""

    def __init__(self, experts, context: Context | None = None, tracer=None):
        if isinstance(experts, type):
            experts = (experts,)
        experts = tuple(experts)
        # A program's module-level `context` is the starting working memory;
        # an explicit context overrides it.
        self.starting: Context = Context()
        if context is None:
            for expert in experts:
                if expert.starting_context is not None:
                    self.starting = expert.starting_context()
                    break
        self.state = State(experts, context, tracer=tracer)
        self.solution: State | None = None

    def run(self) -> Status:
        state = self.state
        if state.tracer is not None:
            state.tracer.header(state.experts[0] if state.experts else State)
        for clause in self.starting:
            state.post(Assert(clause))
        state.post(START)   # rules triggered on `start` run once, on the world as given
        from .space import ProblemSpace

        priority = state.experts[0].priority if state.experts else None
        self.solution = ProblemSpace(state, priority).run()
        return Status.SUCCEEDED if self.solution is not None else Status.FAILED

    @property
    def plan(self):
        """The effects of the solution, ready to replay. Empty before a successful run."""
        from .plan import Plan

        return Plan(self.solution) if self.solution is not None else None
