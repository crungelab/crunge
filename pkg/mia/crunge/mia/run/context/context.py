from __future__ import annotations

from typing import Any, Iterator, Optional

from ...run import term_, Believe, Clause

from .query import Query


class Context:
    """A set of clauses that can be queried by pattern.

    Matching returns bindings or None, never a bool, so every call site here
    tests `is not None` rather than truthiness -- a match that bound nothing
    is still a match.

    Extras travel as keywords (`**x`) the whole way down, which is what
    `Clause.match` and `Trigger.match` agree on. They used to be passed
    positionally from here into a parameter that `Clause.match` never read,
    so they have never actually been compared against anything.
    """

    def __init__(self, clauses: Optional[list[Clause]] = None) -> None:
        # Copy, and never a mutable default: `context_()` builds with no
        # arguments, so a shared default list meant every context in the
        # process believed the same things.
        self.clauses: list[Clause] = list(clauses) if clauses else []

    def __iter__(self) -> Iterator[Clause]:
        yield from self.clauses

    def __len__(self) -> int:
        return len(self.clauses)

    def copy(self) -> "Context":
        return Context(self.clauses)

    def load(self, loader):
        return loader.load(self)

    def config(self, cfg) -> "Context":
        if not cfg:
            return self
        for k in cfg:
            v = cfg[k]
            if k == "clauses":
                for c in v:
                    self.add(c)
                # `break` here, so any key after "clauses" was silently
                # dropped.
                continue
            setattr(self, k, v)
        return self

    #
    # CLAUSES
    #
    def add(self, c):
        if isinstance(c, list):
            self.clauses.extend(c)
        else:
            self.clauses.append(c)
        return self.clauses

    def remove(self, clause) -> "Context":
        self.clauses = [c for c in self.clauses if c != clause]
        return self

    def believe(self, s, v, o=None, x=None) -> "Context":
        self.add(Believe(s, v, o, x))
        return self

    #
    # QUERYING
    #
    def match(self, t, s, v, o=None, **x) -> Iterator[Clause]:
        """Every clause matching the pattern."""
        for c in self.clauses:
            if c.match(t, s, v, o, **x) is not None:
                yield c

    def solve(self, t, s, v, o=None, **x) -> Iterator[tuple[Clause, Any]]:
        """Every match, with what its variables bound to.

        `match` throws the bindings away, which is a loss the moment a
        pattern carries a variable: a query for `$x likes turtles` knows
        what `$x` was and had no way to say so.
        """
        for c in self.clauses:
            bindings = c.match(t, s, v, o, **x)
            if bindings is not None:
                yield c, bindings

    def exists(self, t, s, v, o=None, **x) -> bool:
        return any(c.match(t, s, v, o, **x) is not None for c in self.clauses)

    def find(self, t, s, v, o=None, **x) -> list[Clause]:
        return list(self.match(t, s, v, o, **x))

    def query(self, t, s, v, o=None, **x) -> Query:
        return Query(self)._and(t, s, v, o, **x)

    #
    # SERIALIZATION
    #
    def from_json(self, data) -> "Context":
        for k in data:
            v = data[k]
            t = v.get("type")
            subj = term_(k, t)
            for vk in v:
                if vk == "type":
                    # Read above as the subject's term type; believing it as
                    # a verb as well gave every subject a spurious
                    # `<subj> type <type>` clause.
                    continue
                vv = v[vk]
                verb = term_(vk)
                if isinstance(vv, list):
                    for obj in vv:
                        self.believe(subj, verb, term_(obj))
                else:
                    self.believe(subj, verb, term_(vv))
        return self

    # Legacy spelling.
    fromJSON = from_json

    def __repr__(self) -> str:
        return "\n".join(str(c) for c in self.clauses)


context_ = lambda cfg=None: Context().config(cfg)