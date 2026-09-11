"""Clauses: immutable subject-verb-object facts and goals with optional slots.

Clauses compare and hash by value, so identical clauses are interchangeable in
a context, and copying one returns it unchanged.
"""

from collections.abc import Mapping


class Slots(Mapping):
    """An immutable, hashable mapping of slot names to values."""

    __slots__ = ("_data", "_hash")

    def __init__(self, items=None):
        self._data = dict(items or {})
        self._hash = None

    def __getitem__(self, key):
        return self._data[key]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __hash__(self):
        if self._hash is None:
            self._hash = hash(frozenset(self._data.items()))
        return self._hash

    def __repr__(self):
        return "{" + ", ".join(f"{k}: {v!r}" for k, v in self._data.items()) + "}"

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self


_EMPTY = Slots()


class Clause:
    __slots__ = ("subj", "verb", "obj", "slots", "_hash")

    def __init__(self, subj, verb, obj=None, slots=None):
        init = object.__setattr__
        init(self, "subj", subj)
        init(self, "verb", verb)
        init(self, "obj", obj)
        init(self, "slots", slots if isinstance(slots, Slots) else Slots(slots) if slots else _EMPTY)
        init(self, "_hash", None)

    def __setattr__(self, key, value):
        raise AttributeError(f"{type(self).__name__} is immutable")

    def _key(self):
        return (self.subj, self.verb, self.obj, self.slots)

    def __eq__(self, other):
        return type(self) is type(other) and self._key() == other._key()

    def __hash__(self):
        if self._hash is None:
            object.__setattr__(self, "_hash", hash((type(self), *self._key())))
        return self._hash

    def __repr__(self):
        parts = [repr(self.subj), repr(self.verb)]
        if self.obj is not None:
            parts.append(repr(self.obj))
        parts += [f"{k}: {v!r}" for k, v in self.slots.items()]
        return f"{type(self).__name__}({' '.join(parts)})"

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self


class Belief(Clause):
    __slots__ = ()


class Goal(Clause):
    __slots__ = ()


class Perform(Goal):
    __slots__ = ()


class Achieve(Goal):
    __slots__ = ()


class Query(Goal):
    __slots__ = ()


class Maintain(Goal):
    __slots__ = ()
