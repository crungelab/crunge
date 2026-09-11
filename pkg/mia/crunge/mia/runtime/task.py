"""Tasks: base class for rules compiled to resumable state machines."""

from dataclasses import dataclass
from enum import Enum, auto

from .messages import Attempt, Retract


class Status(Enum):
    SUCCEEDED = auto()
    RETURNED = auto()   # success that leaves the attempted goal in place
    FAILED = auto()
    THROWN = auto()     # this plan doesn't apply; the agent's branch is dead
    SUSPENDED = auto()
    HALTED = auto()     # the problem is solved


SUCCESS = frozenset({Status.SUCCEEDED, Status.RETURNED, Status.HALTED})


@dataclass(frozen=True, slots=True)
class Result:
    succeeded: bool


class Task:
    """Generated subclasses define `trigger`, `bind()`, and `resume()`.

    All of a task's state lives in plain attributes (`pc`, `v_*`, `c_*`), so
    `copy.deepcopy` clones a suspended task.
    """

    trigger = None

    def __init__(self):
        self.pc = 0
        self.message = None
        self.waiter = None

    def bind(self, message) -> bool:
        return True

    def resume(self, agent, result=None) -> Status:
        raise NotImplementedError

    def succeed(self, agent) -> Status:
        # Finishing an attempted goal removes it, as in the C# runtime.
        if isinstance(self.message, Attempt):
            agent.post(Retract(self.message.clause))
        return Status.SUCCEEDED

    def return_(self, agent, value=None) -> Status:
        return Status.RETURNED

    def fail(self, agent) -> Status:
        return Status.FAILED

    def throw(self, agent) -> Status:
        return Status.THROWN

    def __repr__(self):
        return f"{type(self).__qualname__}(pc={self.pc})"
