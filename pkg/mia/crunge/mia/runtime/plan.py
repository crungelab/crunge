"""Plans: the side effects along a solution, ready to be replayed.

Rules record `|` statements as effects instead of performing them, because a
branch that loses the search should leave no trace outside the agent. When an
agency returns a solution, its effects are the plan: the actions of the route
that was actually chosen, in the order the rules recorded them.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Action:
    function: object
    args: tuple

    @property
    def text(self) -> str:
        """The `|` line as written, with the values it was recorded with."""
        source = getattr(self.function, "text", None)
        if source is None:
            return f"{getattr(self.function, '__name__', self.function)}{self.args}"
        names = getattr(self.function, "names", ())
        for name, value in zip(names, self.args):
            source = source.replace(f"${name}", repr(value))
        return source

    def run(self):
        return self.function(*self.args)

    def __repr__(self):
        return f"Action({self.text})"


class Plan:
    """The effects of one solved agent, in order."""

    __slots__ = ("agent", "actions")

    def __init__(self, agent):
        self.agent = agent
        self.actions = [Action(function, args) for function, args in agent.effects]

    def run(self) -> None:
        for action in self.actions:
            action.run()

    def __iter__(self):
        return iter(self.actions)

    def __len__(self):
        return len(self.actions)

    def __repr__(self):
        return f"Plan({len(self.actions)} actions)"

    def __str__(self):
        return "\n".join(action.text for action in self.actions)
