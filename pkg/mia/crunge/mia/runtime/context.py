"""Contexts: sets of clauses indexed by verb."""

from .terms import Sentinel

ANY = Sentinel("ANY")


class Context:
    """An insertion-ordered set of clauses.

    Contexts compare by identity, so a context can be a slot value (as in
    `/blox context: BloxContext`) inside a hashable clause.
    """

    __slots__ = ("_clauses", "_by_verb")

    def __init__(self, clauses=()):
        self._clauses = {}
        self._by_verb = {}
        for clause in clauses:
            self.add(clause)

    def add(self, clause) -> bool:
        if clause in self._clauses:
            return False
        self._clauses[clause] = None
        self._by_verb.setdefault(clause.verb, {})[clause] = None
        return True

    def remove(self, clause) -> bool:
        if clause not in self._clauses:
            return False
        del self._clauses[clause]
        bucket = self._by_verb[clause.verb]
        del bucket[clause]
        if not bucket:
            del self._by_verb[clause.verb]
        return True

    def replace(self, clause) -> list:
        """Remove clauses of the same class, subject, and verb as `clause`, except `clause` itself."""
        old = [
            c for c in self._by_verb.get(clause.verb, ())
            if type(c) is type(clause) and c.subj == clause.subj and c != clause
        ]
        for c in old:
            self.remove(c)
        return old

    def find(self, cls, subj, verb, obj) -> list:
        return [
            c for c in self._by_verb.get(verb, ())
            if isinstance(c, cls)
            and (subj is ANY or c.subj == subj)
            and (obj is ANY or c.obj == obj)
        ]

    def exists(self, cls, subj, verb, obj) -> bool:
        return any(
            isinstance(c, cls) and (subj is ANY or c.subj == subj) and (obj is ANY or c.obj == obj)
            for c in self._by_verb.get(verb, ())
        )

    def copy(self) -> "Context":
        new = Context.__new__(Context)
        new._clauses = dict(self._clauses)
        new._by_verb = {verb: dict(bucket) for verb, bucket in self._by_verb.items()}
        return new

    def __deepcopy__(self, memo):
        return self.copy()

    def __iter__(self):
        return iter(tuple(self._clauses))

    def __len__(self):
        return len(self._clauses)

    def __contains__(self, clause):
        return clause in self._clauses

    def __repr__(self):
        return f"Context({len(self)} clauses)"
