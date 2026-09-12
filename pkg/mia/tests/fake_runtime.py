"""Minimal stand-in for crunge.mia.runtime.

Just enough for generated code to import and run in tests. It doubles as the
list of names the generated code expects the real runtime to provide.
"""


class _Sentinel:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


ANY = _Sentinel("ANY")
START = _Sentinel("START")
IMPASSE = _Sentinel("IMPASSE")


# ---------------------------------------------------------------- terms

class Term:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name


class Entity(Term):
    pass


class Verb(Term):
    pass


_terms = {}


def noun(name, type=None):
    return _terms.setdefault(name, (type or Entity)(name))


def verb(name):
    return _terms.setdefault(name, Verb(name))


SELF = noun("Self")


# ---------------------------------------------------------------- clauses

class Clause:
    def __init__(self, subj, verb, obj=None, slots=None):
        self.subj, self.verb, self.obj, self.slots = subj, verb, obj, slots or {}

    def _key(self):
        return (type(self), self.subj, self.verb, self.obj, tuple(sorted(self.slots.items(), key=str)))

    def __eq__(self, other):
        return isinstance(other, Clause) and self._key() == other._key()

    def __hash__(self):
        return hash((type(self), self.subj, self.verb, self.obj))

    def __repr__(self):
        slots = f" {self.slots}" if self.slots else ""
        return f"{type(self).__name__}({self.subj} {self.verb} {self.obj}{slots})"


class Belief(Clause): pass
class Goal(Clause): pass
class Perform(Goal): pass
class Achieve(Goal): pass
class Query(Goal): pass
class Maintain(Goal): pass


# ---------------------------------------------------------------- messages

class Message:
    def __init__(self, clause):
        self.clause = clause

    def __eq__(self, other):
        return type(self) is type(other) and self.clause == other.clause

    def __repr__(self):
        return f"{type(self).__name__}({self.clause})"


class Attempt(Message): pass
class Assert(Message): pass
class Retract(Message): pass
class Modify(Message): pass


class Trigger:
    def __init__(self, kind, clause_class, verb):
        self.kind, self.clause_class, self.verb = kind, clause_class, verb


# ---------------------------------------------------------------- context, tasks, agents

class Context:
    def __init__(self, clauses=()):
        self.clauses = list(clauses)

    def add(self, clause):
        self.clauses.append(clause)

    def find(self, cls, subj, verb, obj):
        for c in self.clauses:
            if (isinstance(c, cls) and c.verb is verb
                    and (subj is ANY or c.subj == subj)
                    and (obj is ANY or c.obj == obj)):
                yield c

    def exists(self, cls, subj, verb, obj):
        return any(True for _ in self.find(cls, subj, verb, obj))

    def __iter__(self):
        return iter(self.clauses)

    def __len__(self):
        return len(self.clauses)

    def __contains__(self, clause):
        return clause in self.clauses


class Task:
    pc = 0
    trigger = None

    def succeed(self, state): return "SUCCEEDED"
    def return_(self, state, value=None): return "RETURNED"
    def fail(self, state): return "FAILED"
    def throw(self, state): return "THROWN"


class Result:
    def __init__(self, succeeded):
        self.succeeded = succeeded


class Expert:
    entry = None
    rules = ()
    experts = ()
    predicates = {}
    frames = ()
    starting_context = None


class State:
    def __init__(self, experts=(), context=None):
        self.experts = (experts,) if isinstance(experts, type) else tuple(experts)
        self.context = context or Context()
        self.view = self.context
        self.posts = []
        self.proposals = []
        self.effects = []

    def post(self, message, waiter=None):
        self.posts.append(message)
        return "SUSPENDED" if waiter else None

    def propose(self, message, waiter=None):
        self.proposals.append(message)
        return "SUSPENDED" if waiter else None

    def effect(self, function, *args):
        self.effects.append((function, args))

    def halt(self):
        return "HALTED"


class Deliberator(Expert):
    pass
