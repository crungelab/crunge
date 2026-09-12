"""Experts: sets of rules, with no state of their own.

An expert is a class the compiler fills in — its rules, the frames it knows,
the predicates it declares, and any experts nested inside it. Several experts
can be active on one `State` at a time, and a state can gain or lose one while
it runs, so behaviour composes without inheritance.
"""

from __future__ import annotations

from collections.abc import Sequence
from functools import cache

from .task import Task


class Expert:
    entry: type[Task] | None = None   # the rule another expert's message spawns this one through
    rules: tuple[type[Task], ...] = ()
    experts: tuple[type[Expert], ...] = ()   # experts nested inside this one
    predicates: dict = {}
    frames: tuple = ()   # background knowledge, searched after a state's own context
    starting_context = None   # builds the working memory a ProblemSolver starts with
    priority = None   # search priority for this expert's problem space; None means A*

    def __init__(self):
        raise TypeError(f"{type(self).__name__} is a set of rules, not a state; give it to a State")


class Deliberator(Expert):
    pass


@cache
def _own_rules(cls: type[Expert]) -> tuple[type[Task], ...]:
    rules: list[type[Task]] = []
    for klass in reversed(cls.__mro__):
        for rule in vars(klass).get("rules", ()):
            if rule not in rules:
                rules.append(rule)
    return tuple(rules)


@cache
def _own_frames(cls: type[Expert]) -> tuple:
    frames: list = []
    for klass in reversed(cls.__mro__):
        for frame in vars(klass).get("frames", ()):
            if frame not in frames:
                frames.append(frame)
    return tuple(frames)


@cache
def experts_rules(experts: Sequence[type[Expert]]) -> tuple[type[Task], ...]:
    """Every rule of every active expert, in order, without repeats."""
    rules: list[type[Task]] = []
    for expert in experts:
        for rule in _own_rules(expert):
            if rule not in rules:
                rules.append(rule)
    return tuple(rules)


@cache
def experts_frames(experts: Sequence[type[Expert]]) -> tuple:
    frames: list = []
    for expert in experts:
        for frame in _own_frames(expert):
            if frame not in frames:
                frames.append(frame)
    return tuple(frames)
