"""Messages wrap a clause with what to do with it, and triggers match them."""

from .terms import Sentinel

IMPASSE = Sentinel("IMPASSE")


class Message:
    __slots__ = ("clause",)

    def __init__(self, clause):
        object.__setattr__(self, "clause", clause)

    def __setattr__(self, key, value):
        raise AttributeError(f"{type(self).__name__} is immutable")

    def __eq__(self, other):
        return type(self) is type(other) and self.clause == other.clause

    def __hash__(self):
        return hash((type(self), self.clause))

    def __repr__(self):
        return f"{type(self).__name__}({self.clause!r})"

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self


class Attempt(Message):
    __slots__ = ()


class Assert(Message):
    __slots__ = ()


class Retract(Message):
    __slots__ = ()


class Modify(Message):
    __slots__ = ()


class Trigger:
    """Matches messages by message class, clause class, and (optionally) verb."""

    __slots__ = ("kind", "clause_class", "verb")

    def __init__(self, kind, clause_class, verb=None):
        self.kind = kind
        self.clause_class = clause_class
        self.verb = verb

    def matches(self, message) -> bool:
        return (
            isinstance(message, self.kind)
            and isinstance(message.clause, self.clause_class)
            and (self.verb is None or message.clause.verb is self.verb)
        )

    def __repr__(self):
        verb = f" {self.verb}" if self.verb is not None else ""
        return f"Trigger({self.kind.__name__} {self.clause_class.__name__}{verb})"
