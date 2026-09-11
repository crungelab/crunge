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


class View:
    """A read-only union of contexts, searched in order with duplicates dropped.

    An agent's view is its own working memory first, then the frames it knows,
    so a query spans both without the rule saying which space a fact is in.
    """

    __slots__ = ("contexts",)

    def __init__(self, contexts):
        self.contexts = tuple(contexts)

    def find(self, cls, subj, verb, obj) -> list:
        if len(self.contexts) == 1:
            return self.contexts[0].find(cls, subj, verb, obj)
        found, seen = [], set()
        for context in self.contexts:
            for clause in context.find(cls, subj, verb, obj):
                if clause not in seen:
                    seen.add(clause)
                    found.append(clause)
        return found

    def exists(self, cls, subj, verb, obj) -> bool:
        return any(c.exists(cls, subj, verb, obj) for c in self.contexts)

    def __iter__(self):
        seen = set()
        for context in self.contexts:
            for clause in context:
                if clause not in seen:
                    seen.add(clause)
                    yield clause

    def __len__(self):
        return sum(1 for _ in self)

    def __contains__(self, clause):
        return any(clause in c for c in self.contexts)

    def __repr__(self):
        return f"View({len(self.contexts)} contexts)"
