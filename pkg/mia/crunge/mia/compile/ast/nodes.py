"""Mia syntax tree.

The parser builds these nodes and records only what the source says.
Anything that depends on position is left empty for later passes to fill in:
the default performative of a bare message (Attempt in rule bodies, Assert in
contexts), the Self subject of a perform goal, and the subject of paragraph
predicates.
"""

from __future__ import annotations

from dataclasses import dataclass, field, fields
from enum import StrEnum
from typing import Any, Iterator


@dataclass(slots=True)
class Node:
    line: int = field(default=0, kw_only=True, repr=False, compare=False)
    column: int = field(default=0, kw_only=True, repr=False, compare=False)


# ---------------------------------------------------------------- terms


@dataclass(slots=True)
class Var(Node):
    name: str
    type: str | None = None


@dataclass(slots=True)
class Name(Node):
    name: str
    type: str | None = None


@dataclass(slots=True)
class Literal(Node):
    value: bool | int | float | str | None


@dataclass(slots=True)
class Code(Node):
    text: str


# ---------------------------------------------------------------- clauses & goals


@dataclass(slots=True)
class Slot(Node):
    name: str
    value: Term


@dataclass(slots=True)
class Clause(Node):
    subj: Term | None
    verb: str
    objs: list[Term] = field(default_factory=list)
    slots: list[Slot] = field(default_factory=list)
    bind: Var | None = None


class GoalKind(StrEnum):
    PERFORM = "/"
    ACHIEVE = "@"
    QUERY = "?"


@dataclass(slots=True)
class Goal(Node):
    kind: GoalKind
    clause: Clause


type Term = Var | Name | Literal | Code | Clause
type Content = Clause | Goal | Term


# ---------------------------------------------------------------- messages


class Performative(StrEnum):
    ASSERT = "+"
    RETRACT = "-"
    MODIFY = "-+"


@dataclass(slots=True)
class Message(Node):
    content: Content
    propose: bool = False
    performative: Performative | None = None
    paragraph: list[Clause] = field(default_factory=list)


@dataclass(slots=True)
class Trigger(Node):
    content: Content
    performative: Performative | None = None


# ---------------------------------------------------------------- control


@dataclass(slots=True)
class Return(Node):
    value: Term | None = None


@dataclass(slots=True)
class Succeed(Node):
    pass


@dataclass(slots=True)
class Fail(Node):
    pass


@dataclass(slots=True)
class Throw(Node):
    pass


@dataclass(slots=True)
class Halt(Node):
    pass


@dataclass(slots=True)
class Pass(Node):
    pass


@dataclass(slots=True)
class Cost(Node):
    value: Term


@dataclass(slots=True)
class Import(Node):
    path: str


@dataclass(slots=True)
class Snippet(Node):
    text: str
    deferred: bool = False  # `||` records the line as a plan action; `|` runs it now


# ---------------------------------------------------------------- where


@dataclass(slots=True)
class Match(Node):
    clause: Clause


@dataclass(slots=True)
class NoMatch(Node):
    clause: Clause


@dataclass(slots=True)
class Compare(Node):
    left: Term
    op: str
    right: Term


@dataclass(slots=True)
class Filter(Node):
    code: Code


type Condition = Match | NoMatch | Compare | Filter


class Outcome(StrEnum):
    EACH = "-->"
    ANY = "==>"
    NONE = "!==>"


@dataclass(slots=True)
class Branch(Node):
    outcome: Outcome
    body: list[Stmt]


@dataclass(slots=True)
class Where(Node):
    conditions: list[Condition]
    branches: list[Branch]
    frame: str | None = None  # the frame to search, or None for the expert's own context


# ---------------------------------------------------------------- declarations


@dataclass(slots=True)
class Select(Node):
    conditions: list[Condition]
    otherwise: list[Stmt] = field(default_factory=list)  # runs when nothing matches
    frame: str | None = None


@dataclass(slots=True)
class ClassDef(Node):
    name: str
    bases: list[str] = field(default_factory=list)


@dataclass(slots=True)
class PredicateDef(Node):
    name: str
    type: str | None = None


@dataclass(slots=True)
class KnowsDef(Node):
    name: str


@dataclass(slots=True)
class ContextDef(Node):
    name: str
    body: list[Stmt]


@dataclass(slots=True)
class FrameDef(Node):
    name: str
    body: list[Stmt]


@dataclass(slots=True)
class Def(Node):
    name: str
    trigger: Trigger | None
    body: list[Stmt]


@dataclass(slots=True)
class ExpertDef(Node):
    name: str
    bases: list[str]
    body: list[Stmt]


@dataclass(slots=True)
class Module(Node):
    body: list[Stmt]


type Stmt = (
    ExpertDef | ClassDef | PredicateDef | KnowsDef | ContextDef | FrameDef | Def | Where | Select | Message
    | Return | Succeed | Fail | Throw | Halt | Pass | Cost | Import | Snippet
)


# ---------------------------------------------------------------- traversal


def children(node: Node) -> Iterator[Node]:
    for f in fields(node):
        value = getattr(node, f.name)
        if isinstance(value, Node):
            yield value
        elif isinstance(value, list):
            yield from (v for v in value if isinstance(v, Node))


def walk(node: Node) -> Iterator[Node]:
    yield node
    for child in children(node):
        yield from walk(child)


def to_json(value: Any) -> Any:
    if isinstance(value, Node):
        out = {"KIND": type(value).__name__}
        for f in fields(value):
            if f.name not in ("line", "column"):
                out[f.name] = to_json(getattr(value, f.name))
        return out
    if isinstance(value, list):
        return [to_json(v) for v in value]
    return value
