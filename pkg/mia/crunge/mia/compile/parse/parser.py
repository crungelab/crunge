"""Lark front end for Mia: source text in, `nodes.Module` out."""

from ast import literal_eval
from pathlib import Path

from lark import Lark, Token, Transformer, Tree, v_args
from lark.exceptions import VisitError
from lark.indenter import Indenter

from crunge.mia.compile.ast.nodes import (
    AgentDef, Branch, ClassDef, Clause, Code, Compare, ContextDef, Cost, Def,
    ExpertDef, Fail, Filter, FrameDef, Goal, GoalKind, Halt, Import, KnowsDef, Literal, Match,
    Message, Module, Name, NoMatch, Outcome, Pass, Performative, PredicateDef,
    Return, Slot, Snippet, Succeed, Throw, Trigger, Var, Where,
)


class MiaSyntaxError(SyntaxError):
    pass


class MiaIndenter(Indenter):
    NL_type = "_NL"
    OPEN_PAREN_types = ["LPAR"]
    CLOSE_PAREN_types = ["RPAR"]
    INDENT_type = "_INDENT"
    DEDENT_type = "_DEDENT"
    tab_len = 4


def _pos(meta) -> dict:
    # Rules that matched no tokens have an empty meta with no line attribute.
    return {"line": getattr(meta, "line", 0), "column": getattr(meta, "column", 0)}


def _term(x):
    """Convert a raw token in term position; nodes pass through."""
    if not isinstance(x, Token):
        return x
    pos = {"line": x.line, "column": x.column}
    match x.type:
        case "VAR":
            return Var(x[1:], **pos)
        case "NOUN":
            return Name(str(x), **pos)
        case "CODE":
            return Code(x[1:-1].strip(), **pos)
    raise MiaSyntaxError(f"line {x.line}: unexpected {x.type} {x!r} in term position")


@v_args(inline=True, meta=True)
class ToAst(Transformer):
    # ------------------------------------------------------------ structure

    def start(self, meta, *stmts):
        return Module(list(stmts), **_pos(meta))

    def suite(self, meta, *stmts):
        return list(stmts)

    def agent_def(self, meta, name, bases, body):
        return AgentDef(str(name), bases or [], body, **_pos(meta))

    def expert_def(self, meta, name, bases, body):
        return ExpertDef(str(name), bases or [], body, **_pos(meta))

    def class_def(self, meta, name, bases):
        return ClassDef(str(name), bases or [], **_pos(meta))

    def bases(self, meta, *names):
        return [str(x) for x in names]

    def predicate_decl(self, meta, name, type_ref):
        return PredicateDef(str(name), str(type_ref) if type_ref else None, **_pos(meta))

    def knows_decl(self, meta, name):
        return KnowsDef(str(name), **_pos(meta))

    def def_def(self, meta, name, trigger, body):
        return Def(str(name), trigger, body, **_pos(meta))

    def context_def(self, meta, name, body):
        return ContextDef(str(name), body, **_pos(meta))

    def frame_def(self, meta, name, body):
        return FrameDef(str(name), body, **_pos(meta))

    def trigger(self, meta, performative, content):
        return Trigger(_term(content), performative, **_pos(meta))

    # ------------------------------------------------------------ where

    def where_stmt(self, meta, frame, *items):
        conditions = [x for x in items if not isinstance(x, Branch)]
        branches = [x for x in items if isinstance(x, Branch)]
        return Where(conditions, branches, str(frame) if frame else None, **_pos(meta))

    def match(self, meta, clause):
        return Match(clause, **_pos(meta))

    def no_match(self, meta, clause):
        return NoMatch(clause, **_pos(meta))

    def compare(self, meta, left, op, right):
        return Compare(_term(left), str(op), _term(right), **_pos(meta))

    def filter(self, meta, code):
        return Filter(_term(code), **_pos(meta))

    def each_match(self, meta, *body):
        return Branch(Outcome.EACH, list(body), **_pos(meta))

    def any_match(self, meta, *body):
        return Branch(Outcome.ANY, list(body), **_pos(meta))

    def none_match(self, meta, *body):
        return Branch(Outcome.NONE, list(body), **_pos(meta))

    # ------------------------------------------------------------ statements

    def simple_stmt(self, meta, action, paragraph):
        if paragraph:
            if not isinstance(action, Message):
                raise MiaSyntaxError(f"line {meta.line}: only a message can have a paragraph")
            action.paragraph = paragraph
        return action

    def paragraph(self, meta, *predicates):
        return list(predicates)

    def predicate(self, meta, verb, objs, *slots):
        return Clause(None, str(verb), objs or [], list(slots), **_pos(meta))

    def message(self, meta, propose, performative, content):
        return Message(_term(content), propose is not None, performative, **_pos(meta))

    def performative(self, meta, token):
        return Performative(str(token))

    def return_stmt(self, meta, value):
        return Return(_term(value) if value is not None else None, **_pos(meta))

    def succeed_stmt(self, meta):
        return Succeed(**_pos(meta))

    def fail_stmt(self, meta):
        return Fail(**_pos(meta))

    def throw_stmt(self, meta):
        return Throw(**_pos(meta))

    def halt_stmt(self, meta):
        return Halt(**_pos(meta))

    def pass_stmt(self, meta):
        return Pass(**_pos(meta))

    def cost_stmt(self, meta, value):
        return Cost(_term(value), **_pos(meta))

    def import_stmt(self, meta, path):
        return Import(path, **_pos(meta))

    def dotted(self, meta, *parts):
        return ".".join(parts)

    def snippet(self, meta, token):
        return Snippet(token[1:].strip(), **_pos(meta))

    # ------------------------------------------------------------ goals, clauses, terms

    def perform(self, meta, verb, objs, *rest):
        *slots, bind = rest
        clause = Clause(None, str(verb), objs or [], slots, bind, **_pos(meta))
        return Goal(GoalKind.PERFORM, clause, **_pos(meta))

    def achieve(self, meta, clause):
        return Goal(GoalKind.ACHIEVE, clause, **_pos(meta))

    def query(self, meta, clause):
        return Goal(GoalKind.QUERY, clause, **_pos(meta))

    def clause(self, meta, subj, verb, objs, *rest):
        *slots, bind = rest
        return Clause(_term(subj) if subj is not None else None, str(verb),
                      objs or [], slots, bind, **_pos(meta))

    def objects(self, meta, *terms):
        return [_term(t) for t in terms]

    def slot(self, meta, name, value):
        return Slot(name[:-1], _term(value), **_pos(meta))

    def binding(self, meta, var):
        return _term(var)

    def typed(self, meta, type_name, token):
        term = _term(token)
        term.type = str(type_name)
        return term

    def literal(self, meta, token):
        # Mia literals (True, False, None, numbers, strings) are Python literals.
        return Literal(literal_eval(token), **_pos(meta))


_lark = Lark.open(
    Path(__file__).with_name("mia.lark"),
    parser="lalr",
    postlex=MiaIndenter(),
    propagate_positions=True,
    maybe_placeholders=True,
)


def parse_raw(text: str) -> Tree:
    """The Lark parse tree, before it is turned into syntax-tree nodes.

    Useful for inspecting the grammar's own view of a program — `print(tree.pretty())`
    — when a rule matches differently than expected. Use `parse` for compiling.
    """
    if not text.endswith("\n"):
        text += "\n"
    return _lark.parse(text)


def parse(text: str) -> Module:
    tree = parse_raw(text)
    try:
        return ToAst().transform(tree)
    except VisitError as e:
        raise e.orig_exc from None
