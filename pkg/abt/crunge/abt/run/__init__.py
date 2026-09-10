from typing import Pattern, Callable
import json

class Failure(Exception):
    pass

__ = None


class Variable:
    def __init__(self, name: str, pattern=None):
        self.name = name
        self.pattern = pattern


var_ = lambda name, pattern=None: Variable(name, pattern)


class Bindings:
    __slots__ = ("values",)

    def __init__(self, values=None):
        self.values = values if values is not None else {}

    def bind(self, name, value):
        self.values[name] = value
        return self

    def __bool__(self) -> bool:
        return True          # success with no bindings is still success

    def __getitem__(self, name):
        return self.values[name]

    def __contains__(self, name) -> bool:
        return name in self.values

    def __repr__(self):
        return f"<Bindings {self.values}>"


def unify(p: Callable | Pattern | Variable, v, b: Bindings) -> Bindings | None:
    if p is __ or p == v:
        return b
    if isinstance(p, Variable):
        if p.pattern and unify(p.pattern, v, b) is None:
            return None
        if p.name in b and b[p.name] != v:
            return None      # $x twice must mean the same thing
        return b.bind(p.name, v)
    if isinstance(p, Pattern) and p.test(v):
        return b
    if callable(p) and p(v):
        return b
    return None

'''
def match(p: Callable | Pattern | Variable, v, b=True):
    if p == __ or p == v:
        return b
    if callable(p) and p(v):
        return b
    if isinstance(p, Pattern) and p.test(v):
        return b
    if isinstance(p, Variable):
        if p.pattern and not match(p.pattern, v):
            return False
        if type(b) == object:
            b[p.name] = v
            return b
        return {p.name: v}

    return False
'''

class Term:
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def to_json(self):
        return {'TYPE': self.__class__.__name__, 'NAME': self.name}


class Subject(Term):
    pass


class Verb(Term):
    pass


#
# Object to Term
#
terms = {}


def term_(arg: str | list, T=None):
    term = None
    if type(arg) is str:
        term = terms.get(arg)
        if not term:
            if not T:
                if arg[0].isupper():
                    T = Subject
                else:
                    T = Verb
            elif type(T) is str:
                klass = terms.get(T)
                if not klass:
                    klass = type(T, (Term,), {})
                    terms[T] = klass
                    T = klass
                else:
                    T = klass
            terms[arg] = term = T(arg)
    elif type(arg) is list:
        term = {}
        for e in arg:
            n = "_" + e
            term[n] = term_(e)
    return term


_I = term_("I")
_start = term_("start")
_impasse = term_("impasse")

#
# Clause
#


class Clause:
    def __init__(self, subj: object, verb: object, obj: object = None, xtra=None):
        self.subj = subj
        self.verb = verb
        self.obj = obj
        if xtra:
            for key in xtra:
                setattr(self, key, xtra[key])

        #self.xtra = kwargs

    def __repr__(self):
        xtra = []
        for k in self.__dict__:
            v = self.__dict__[k]
            if (k != "subj") and (k != "verb") and (k != "obj"):
                xtra.append(f"{k} {v}")

        return " ".join(
            [
                self.__class__.__name__,
                str(self.subj),
                str(self.verb),
                str(self.obj),
                str(xtra),
            ]
        )

    def to_json(self):
        return json.dumps({
            "TYPE": self.__class__.__name__,
            "SUBJ": self.subj if self.subj is not None else None,
            "VERB": self.verb if self.verb is not None else None,
            "OBJ": self.obj if self.obj is not None else None,
        })

    def match(self, T, s, v, o=None, **x) -> Bindings | None:
        if not isinstance(self, T):
            return None
        b = Bindings()
        for pattern, value in ((s, self.subj), (v, self.verb), (o, self.obj)):
            b = unify(pattern, value, b)
            if b is None:
                return None
        for key, pattern in x.items():
            b = unify(pattern, getattr(self, key, None), b)
            if b is None:
                return None
        return b

    '''
    def match(self, T: type["Clause"], s: object, v: object, o: object = None, x=None):
        return isinstance(self, T) and match(
            s, self.subj, match(v, self.verb, match(o, self.obj))
        )
    '''

    def __eq__(self, other: 'Clause') -> bool: 
        return (
            self.__class__.__name__ == other.__class__.__name__
            and self.subj == other.subj
            and self.verb == other.verb
            and self.obj == other.obj
        )

    def __hash__(self):
        # necessary for instances to behave sanely in dicts and sets.
        return hash((self.subj, self.verb, self.obj))


clause_ = lambda T, s, v, o=None, **x: T(s, v, o, x)
#
class Believe(Clause):
    pass


believe_ = lambda s, v, o=None, **x: Believe(s, v, o, x)
#
class Goal(Clause):
    pass


#
class Achieve(Goal):
    pass

from .message import *
