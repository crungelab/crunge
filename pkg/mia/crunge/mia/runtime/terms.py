"""Terms: interned nouns and verbs.

A term is identified by its name (and, for nouns, its type), so every
reference to Block1 is the same object and compares by identity. Terms are
immutable, and copying one returns it unchanged.
"""


class Sentinel:
    __slots__ = ("name",)

    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self


class Term:
    __slots__ = ("name",)

    def __init__(self, name: str):
        object.__setattr__(self, "name", name)

    def __setattr__(self, key, value):
        raise AttributeError(f"{type(self).__name__} {self.name} is immutable")

    def __repr__(self):
        return self.name

    def __copy__(self):
        return self

    def __deepcopy__(self, memo):
        return self


class Entity(Term):
    """Base class for declared Mia types."""

    __slots__ = ()


class Verb(Term):
    __slots__ = ()


_nouns: dict[tuple[str, type], Term] = {}
_verbs: dict[str, Verb] = {}


def noun(name: str, cls: type[Entity] = Entity) -> Entity:
    # Keyed by class too, so re-executing a generated module (new class
    # objects) gets fresh terms instead of clashing with the old ones.
    key = (name, cls)
    term = _nouns.get(key)
    if term is None:
        term = _nouns[key] = cls(name)
    return term


def verb(name: str) -> Verb:
    term = _verbs.get(name)
    if term is None:
        term = _verbs[name] = Verb(name)
    return term


SELF = noun("Self")
