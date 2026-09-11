import json

from . import Clause
#
# Message
#
class Message:
    def __init__(self, data: Clause, sender=None, to=None):
        self.data = data
        self.sender = sender
        self.to = to

    def __repr__(self):
        return " ".join([self.__class__.__name__, str(self.data)])


    def to_json(self):
        return json.dumps({
            "TYPE": self.__class__.__name__,
            "DATA": self.data if self.data is not None else None,
            "TO": self.to if self.to is not None else None,
            "FROM": self.sender if self.sender is not None else None,
        })

    def match(self, F: type["Message"], T: type[Clause], s: object, v: object, o: object = None, **x) -> bool:
        return isinstance(self, F) and self.data.match(T, s, v, o, **x)


class Propose(Message):
    pass


propose_ = lambda T, s, v, o=None, **x: Propose(T(s, v, o, **x))


class Attempt(Message):
    pass


attempt_ = lambda T, s, v, o=None, **x: Attempt(T(s, v, o, **x))


class Assert(Message):
    pass


assert_ = lambda T, s, v, o=None, **x: Assert(T(s, v, o, **x))


class Retract(Message):
    pass


retract_ = lambda T, s, v, o=None, x=None: Retract(T(s, v, o, x))

#
# Trigger
#
class Trigger:
    def __init__(self, flavor: type[Message], T: type[Clause], subj: object, verb: object, obj: object, **xtra):
        self.flavor = flavor  # message type
        self.type = T  # clause type
        self.subj = subj
        self.verb = verb
        self.obj = obj
        self.xtra = xtra

    def match(self, msg: Message) -> bool:
        return msg.match(
            self.flavor, self.type, self.subj, self.verb, self.obj, **self.xtra
        )


#
class OnAssert(Trigger):
    def __init__(self, T, s, v, o=None, **x):
        super().__init__(Assert, T, s, v, o, **x)


onAssert_ = lambda T, s, v, o=None, **x: OnAssert(T, s, v, o, **x)
#
class OnRetract(Trigger):
    pass


onRetract_ = lambda T, s, v, o=None, **x: OnRetract(T, s, v, o, **x)


class OnAttempt(Trigger):
    def __init__(self, T, s, v, o=None, **x):
        super().__init__(Attempt, T, s, v, o, **x)


onAttempt_ = lambda T, s, v, o=None, **x: OnAttempt(T, s, v, o, **x)

destruct = lambda dict, *args: (dict[arg] for arg in args)