from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Iterator, Optional

import inspect
import types
from copy import copy

if TYPE_CHECKING:
    from crunge.core import BaseNode

from .message import Message, Trigger

class Match:
    __slots__ = ("msg", "rule", "bindings")

    def __init__(self, msg, rule, bindings=None):
        self.msg = msg
        self.rule = rule
        self.bindings = bindings if bindings else {}

    def __repr__(self) -> str:
        return f"<Match {self.rule} {self.msg} {self.bindings}>"

'''
class Match:
    __slots__ = ("msg", "rule")

    def __init__(self, msg: Message, rule: "Rule"):
        self.msg = msg
        self.rule = rule

    def __repr__(self) -> str:
        return f"<Match {self.rule} {self.msg}>"
'''

#
# Rule
#
class Rule:
    """One trigger bound to one action.

    `action` is the raw function off the class body, unbound. It is not a
    method of anything until someone binds it -- see `bind` and the note on
    the calling convention in the module docstring.
    """

    def __init__(
        self,
        trigger: Trigger,
        action: Callable,
        prodname: Optional[str] = None,
        filename: Optional[str] = None,
        lineno: Optional[int] = None,
    ):
        if not isinstance(trigger, Trigger):
            raise TypeError(f"trigger must be a Trigger, got {trigger!r}")
        self.trigger = trigger
        self.action = action
        self.prodname = prodname
        self.filename = filename
        self.lineno = lineno

    def match(self, msg: Message) -> Optional[Match]:
        result = self.trigger.match(msg)
        if not result:
            return None
        return Match(msg, self, result if isinstance(result, dict) else None)

    '''
    def match(self, msg: Message) -> Optional[Match]:
        if not self.trigger.match(msg):
            return None
        return Match(msg, self)
    '''

    '''
    def match(self, msg: Message) -> Optional[Message]:
        """The message stamped with this rule, or None.

        A copy, so the same message can match several rules and each match
        carries its own provenance.
        """
        if not self.trigger.match(msg):
            return None
        stamped = copy(msg)
        stamped.rule = self
        return stamped
    '''

    def bind(self, node: "BaseNode") -> Callable:
        """The action as a method of `node`.

        The kit is shared across every instance of a class, so binding
        cannot happen when the rule is declared. It happens when the rule
        fires, against whichever node is firing it.
        """
        return types.MethodType(self.action, node)

    def __repr__(self) -> str:
        where = f"{self.filename}:{self.lineno}" if self.filename else "?"
        return f"<Rule {self.prodname or self.action!r} @ {where}>"


#
# RuleKit
#
class RuleKit:
    """A set of rules, owned by a class or by a single node.

    Declared rules live on the class, shared by every instance -- they come
    from the class body and never vary. `owner` records who that is, and is
    what makes inheritance work: a subclass that declares a rule of its own
    forks the kit it inherited rather than appending to it.

    Without the fork, every subclass mutates its parent's list through the
    MRO and all rules pool globally across every class in the tree. That was
    the original bug, and the `# TODO: find rules in super classes` comment
    was diagnosing its symptom backwards -- rules were not under-inherited,
    they were shared by everything.

    A node that gains a rule at run time (through `Act.define`, say) forks
    the same way, into a kit owned by the instance:

        def add_rule(self, rule):
            kit = self._rules
            if kit is None:
                inherited = self.get_cls_chip(RuleKit)
                kit = self._rules = (
                    inherited.fork(self) if inherited else RuleKit(owner=self)
                )
            return kit.add_rule(rule)

        def match_rules(self, msg):
            kit = self._rules or self.get_cls_chip(RuleKit)
            return kit.match(msg) if kit is not None else ()

    Shared until written to, private after. `fork` copies the list, so a
    node that subscribes cannot leak a rule into its siblings.
    """

    def __init__(self, rules: Any = None, owner: Any = None) -> None:
        # Copy, never alias. The original handed the provider's own list to
        # every kit it produced, so one instance subscribing at run time
        # rewrote the rules of every other instance and every future one.
        self.rules: list[Rule] = list(rules) if rules is not None else []
        self.owner = owner

    def fork(self, owner: Any) -> "RuleKit":
        return RuleKit(self.rules, owner)

    def add_rule(self, rule: Rule) -> Rule:
        self.rules.append(rule)
        return rule

    def remove_rule(self, rule: Rule) -> "RuleKit":
        self.rules.remove(rule)
        return self

    def match(self, msg: Message) -> Iterator[Message]:
        """Every rule that fires, as stamped messages, in declaration order.

        One method where there were four. `find_rules` and `match_rules`
        returned different things -- Rules and stamped Messages -- and
        `match_rule` called `.pop()` on a generator, so it could never have
        run. Callers that want just the first take `next(kit.match(msg),
        None)`.
        """
        for rule in self.rules:
            stamped = rule.match(msg)
            if stamped is not None:
                yield stamped

    def __len__(self) -> int:
        return len(self.rules)

    def __repr__(self) -> str:
        owner = getattr(self.owner, "__name__", None) or repr(self.owner)
        return f"<RuleKit {owner} rules={len(self.rules)}>"


def _kit_for(cls: type) -> RuleKit:
    """This class's own kit, forking an inherited one on first write."""
    kit = cls.get_cls_chip(RuleKit)
    if kit is None:
        kit = RuleKit(owner=cls)
    elif kit.owner is not cls:
        kit = kit.fork(cls)
    else:
        return kit
    cls.add_cls_chip(kit, key=RuleKit)
    return kit


#
# Decorator
#
def rule(trigger: Trigger, *extra: Trigger):
    """Declare a rule in a class body.

        class Forager(Act):
            @rule(Attempt(Achieve("eat")))
            async def eat(self, msg):
                ...

    `inject` is called by BaseNode.__init_subclass__, which scans the class
    body for anything carrying it. By then the class-chip tier has already
    merged its parents in, so `_kit_for` sees an inherited kit and knows to
    fork it.
    """
    triggers = (trigger, *extra)

    def inject(cls: type, func: Callable) -> None:
        unwrapped = inspect.unwrap(func)
        code = unwrapped.__code__
        kit = _kit_for(cls)
        # One rule per trigger. The original built the list and then used
        # triggers[0], so every trigger after the first was dropped without
        # a word.
        for each in triggers:
            kit.add_rule(
                Rule(
                    each,
                    func,
                    prodname=func.__name__,
                    filename=code.co_filename,
                    lineno=code.co_firstlineno,
                )
            )

    def decorate(func: Callable) -> Callable:
        func.inject = inject
        return func

    return decorate