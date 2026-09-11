from __future__ import annotations

from typing import Any, Callable, Iterator, Optional

from ...run import *


class Query:
    """A chain of conditions over a Context.

    Each condition pulls binders from the one before it, so the chain is a
    pipeline: the first draws from a single empty binder, and every one
    after narrows or extends what reached it.
    """

    def __init__(self, ctx) -> None:
        self.ctx = ctx
        self.conds: list["Condition"] = []

    def __iter__(self) -> Iterator[dict]:
        return self.binders()

    def add(self, c: "Condition") -> "Condition":
        c.query = self
        c.ctx = self.ctx
        c.src = self.conds[-1] if self.conds else None
        self.conds.append(c)
        return c

    def _and(self, t, s, v, o=None, **x) -> "Query":
        self.add(QClause(t, s, v, o, **x))
        return self

    def _not(self, t, s, v, o=None, **x) -> "Query":
        # `self.conds[-1]` unguarded, so a query opening with _not raised
        # IndexError. add() handles the empty case now.
        self.add(QNegClause(t, s, v, o, **x))
        return self

    def filter(self, fn: Callable[[dict], bool]) -> "Query":
        self.add(QFilter(fn))
        return self

    def binders(self) -> Iterator[dict]:
        if not self.conds:
            return iter(())
        return self.conds[-1].binders()

    def first(self) -> Optional[dict]:
        return next(self.binders(), None)

    def all(self) -> list[dict]:
        return list(self.binders())

    def exec(self, on_success: Callable[[dict], Any]):
        """First solution only, passed to the callback."""
        binder = self.first()
        if binder is None:
            return None
        return on_success(binder)

    def __repr__(self) -> str:
        return f"<Query conds={len(self.conds)}>"


query_ = lambda ctx: Query(ctx)


class Condition:
    def __init__(self) -> None:
        self.src: Optional["Condition"] = None
        self.query: Optional[Query] = None
        self.ctx = None

    def _source(self) -> Iterator[dict]:
        """Binders from upstream, or one empty binder if we are first."""
        if self.src is not None:
            yield from self.src.binders()
        else:
            yield {}

    def _resolve(self, binder: dict, pattern):
        """Substitute a variable that upstream has already bound.

        Two fixes over `self.binding(binder, p) or p`: it called `p.name` on
        patterns that are not Variables at all, and a legitimately falsy
        binding (0, "") fell back to the unbound pattern.
        """
        if isinstance(pattern, Variable) and pattern.name in binder:
            return binder[pattern.name]
        return pattern

    def binders(self) -> Iterator[dict]:
        raise NotImplementedError


class QFilter(Condition):
    def __init__(self, fn: Callable[[dict], bool]) -> None:
        super().__init__()
        self.fn = fn

    def binders(self) -> Iterator[dict]:
        for binder in self._source():
            if self.fn(binder):
                yield binder


class QClause(Condition):
    """Match a pattern, extending each binder with whatever it binds.

    The four-way isinstance(Variable) tree this replaces was doing the
    matcher's job by hand -- reading `c.subj` and `c.obj` back off the
    clause and rebuilding the bindings that `unify` had already computed and
    thrown away. `Context.solve` hands them over, so binding a variable
    anywhere in the pattern, including an extra, now works the same way.
    """

    def __init__(self, t, s, v, o=None, **x) -> None:
        super().__init__()
        self.t = t
        self.s = s
        self.v = v
        self.o = o
        self.x = x

    def binders(self) -> Iterator[dict]:
        for binder in self._source():
            s = self._resolve(binder, self.s)
            v = self._resolve(binder, self.v)
            o = self._resolve(binder, self.o)
            for _clause, bindings in self.ctx.solve(self.t, s, v, o, **self.x):
                # New bindings last. Anything already bound upstream was
                # substituted into the pattern above, so the two cannot
                # disagree -- previously `result.update(binder)` let upstream
                # overwrite a binding taken from the clause just matched,
                # and the binder could end up describing a clause that was
                # never found.
                merged = dict(binder)
                merged.update(bindings.values)
                yield merged


class QNegClause(Condition):
    """Yield a binder only when the pattern matches nothing.

    Negation as failure, and it binds nothing by definition -- there is no
    matching clause to read values from. Three of the four branches this
    replaces were copy-pasted from QClause and yielded *positive* matches,
    so `_not` behaved as `_and` for any pattern carrying a variable. Only
    the all-literal case was ever negated.
    """

    def __init__(self, t, s, v, o=None, **x) -> None:
        super().__init__()
        self.t = t
        self.s = s
        self.v = v
        self.o = o
        self.x = x

    def binders(self) -> Iterator[dict]:
        for binder in self._source():
            s = self._resolve(binder, self.s)
            v = self._resolve(binder, self.v)
            o = self._resolve(binder, self.o)
            if not self.ctx.exists(self.t, s, v, o, **self.x):
                yield binder