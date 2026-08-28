from typing import Any, Callable, List, Optional, Union, Coroutine

import inspect
from copy import copy

from loguru import logger

from ..run.policy_meta import PolicyMeta
from . import Message


#
# Rule
#
class Rule:
    def __init__(self, trigger, action, prodname=None, filename=None, lineno=None):
        self.trigger = trigger
        self.action = action
        self.prodname = prodname
        self.filename = filename
        self.lineno = lineno

    def match(self, msg: Message):
        result = self.trigger.match(msg)
        if not result:
            return False
        m = copy(msg)
        m.rule = self
        return m


#
# Policy
#
class Policy(metaclass=PolicyMeta):
    def __init__(self):
        super().__init__()
        self.rules: List[Rule] = self.__class__.rules

    def add_rule(self, r: Rule):
        self.rules.append(r)

    def remove_rule(self, r: Rule):
        try:
            self.rules.remove(r)
        except ValueError as e:
            print(e)
            exit()
        return self

    def subscribe(self, trigger, action):
        rule = Rule(trigger, action)
        self.add_rule(rule)
        return rule

    def unsubscribe(self, rule):
        self.remove_rule(rule)

    def find_rule(self, m: Message) -> Rule:
        return self.find_rules(m).pop()

    def find_rules(self, msg: Message):
        result = []
        for r in self.rules:
            if r.match(msg):
                result.append(r)
        return result

    def match_rule(self, msg: Message) -> Rule:
        return self.match_rules(msg).pop()

    def match_rules(self, msg: Message):
        for r in self.rules:
            m = r.match(msg)
            if m:
                logger.debug(f"rule match: {r} {m}")
                yield m

    @classmethod
    def __build_rules(cls, functions: List[Callable]) -> List[Rule]:
        rules = []
        for name, func in functions:
            rule = _build_rule(func)
            rules.append(rule)
        return rules

    @classmethod
    def __collect_functions(cls, definitions) -> List[Callable]:
        functions = [
            (name, value)
            for name, value in definitions
            if callable(value) and hasattr(value, "triggers")
        ]
        return functions

    @classmethod
    def _build(cls, definitions):
        if vars(cls).get("_build", False):
            return

        # Collect all of the rule functions from the class definition
        functions = cls.__collect_functions(definitions)
        # logger.debug(f'functions {functions}')

        cls.rules = cls.__build_rules(functions)


def _build_rule(func: Callable):
    triggers = []
    prodname = func.__name__
    unwrapped = inspect.unwrap(func)
    filename = unwrapped.__code__.co_filename
    lineno = unwrapped.__code__.co_firstlineno
    for trigger, lineno in zip(
        func.triggers, range(lineno + len(func.triggers) - 1, 0, -1)
    ):
        logger.debug(f"trigger: {trigger}")
        triggers.append(trigger)

    rule = Rule(triggers[0], func, prodname=prodname, filename=filename, lineno=lineno)
    logger.debug(f"rule: {rule}")
    return rule
