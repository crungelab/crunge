"""Render runtime values in Mia syntax, for traces and debugging."""

from .clauses import Achieve, Clause, Maintain, Perform, Query
from .context import Context
from .messages import IMPASSE, Assert, Attempt, Message, Modify, Retract
from .terms import Term

_PREFIXES = {Attempt: "", Assert: "+ ", Retract: "- ", Modify: "-+ "}


def to_mia(value) -> str:
    """`@Block1 onTop Block2`, `/clear Block1`, `+ (/countTo 5) value 0`, and so on."""
    match value:
        case _ if value is IMPASSE:
            return "impasse"
        case Message():
            return _PREFIXES.get(type(value), f"{type(value).__name__} ") + to_mia(value.clause)
        case Perform():
            return "/" + _body(value, subject=False)
        case Achieve():
            return "@" + _body(value)
        case Query():
            return "?" + _body(value)
        case Maintain():
            return "maintain " + _body(value)
        case Clause():
            return _body(value)
        case Term():
            return value.name
        case Context():
            return f"<context of {len(value)}>"
        case bool() | None | str():
            return repr(value)
        case tuple():
            return ", ".join(to_mia(v) for v in value)
        case _:
            return str(value)


def _body(clause: Clause, subject: bool = True) -> str:
    parts = [_nested(clause.subj)] if subject else []
    parts.append(clause.verb.name)
    if clause.obj is not None:
        parts.append(_nested(clause.obj))
    parts += [f"{name}: {_nested(value)}" for name, value in clause.slots.items()]
    return " ".join(parts)


def _nested(value) -> str:
    return f"({to_mia(value)})" if isinstance(value, Clause) else to_mia(value)
