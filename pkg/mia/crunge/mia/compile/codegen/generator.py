"""Generate Python source from a Mia syntax tree.

The generated module imports the runtime as `rt` and defines:

* one class per declared type, subclassing `rt.Entity` unless given bases
* one module-level term per noun and verb (`t_Table1`, `t_onTop`)
* one `rt.Agent` subclass per agent or expert, with experts nested
* one `rt.Task` subclass per rule, compiled to a resumable state machine

Generated names can't collide with each other or with Python: terms are
`t_<name>`, variables `v_<name>`, contexts `self.c_<name>`, and compiler
temporaries start with an underscore, which no term or variable name does.

Suspension: a message that waits for a result (an attempt or a proposal)
suspends the task only when it is a top-level statement of the rule body.
Inside a where branch it is sent without waiting, as in the C# version.
Each top-level suspension point ends one `case` of `resume`.

Where: matches are collected into a list before any branch runs, so branch
bodies can change the context without disturbing the query.
"""

from __future__ import annotations

import re
from contextlib import contextmanager
from dataclasses import dataclass, field

from crunge.mia.compile.ast.nodes import (
    AgentDef, ClassDef, Clause, Code, Compare, ContextDef, Def, ExpertDef, Fail,
    Filter, Goal, GoalKind, Halt, Import, Literal, Match, Message, Module, Name,
    Node, NoMatch, Outcome, Pass, Performative, PredicateDef, Return, Snippet,
    Succeed, Throw, Var, Where, walk,
)


class MiaCompileError(Exception):
    def __init__(self, node: Node, message: str):
        super().__init__(f"line {node.line}: {message}")


PY_TYPES = {"bool", "int", "float", "str"}
CLAUSE_TYPES = {"Clause", "Belief", "Goal", "Perform", "Achieve", "Query", "Maintain"}
RUNTIME_TYPES = CLAUSE_TYPES | {"Entity", "Agent", "Deliberator"}

MESSAGE_CLASSES = {
    None: "rt.Attempt",
    Performative.ASSERT: "rt.Assert",
    Performative.RETRACT: "rt.Retract",
    Performative.MODIFY: "rt.Modify",
}
GOAL_CLASSES = {
    GoalKind.PERFORM: "rt.Perform",
    GoalKind.ACHIEVE: "rt.Achieve",
    GoalKind.QUERY: "rt.Query",
}
TERMINATORS = (Return, Succeed, Fail, Throw, Halt)

_DOLLAR = re.compile(r"\$([A-Za-z_]\w*)")


def generate(
    module: Module,
    filename: str = "<mia>",
    source: str | None = None,
    runtime: str = "crunge.mia.runtime",
) -> str:
    """Return Python source for `module`. Pass `source` to get Mia lines as comments."""
    return _Generator(filename, source, runtime).module(module)


class _Writer:
    def __init__(self):
        self.lines: list[str] = []
        self.depth = 0

    def __call__(self, line: str = ""):
        self.lines.append("    " * self.depth + line if line else "")

    @contextmanager
    def block(self, header: str):
        self(header)
        self.depth += 1
        try:
            yield
        finally:
            self.depth -= 1

    def text(self) -> str:
        return "\n".join(self.lines) + "\n"


@dataclass
class _Scope:
    task: dict[str, None] = field(default_factory=dict)  # ordered set of task variables
    locals: set[str] = field(default_factory=set)
    contexts: set[str] = field(default_factory=set)

    def child(self, names=()) -> _Scope:
        return _Scope(self.task, self.locals | set(names), self.contexts)

    def bound(self, name: str) -> bool:
        return name in self.locals or name in self.task


def _tuple(items: list[str]) -> str:
    if len(items) == 1:
        return f"({items[0]},)"
    return "(" + ", ".join(items) + ")"


def _is_blank(term) -> bool:
    return isinstance(term, Var) and term.name == "_"


class _Generator:
    def __init__(self, filename: str, source: str | None, runtime: str):
        self.filename = filename
        self.source_lines = source.splitlines() if source else []
        self.runtime = runtime
        self.w = _Writer()
        self.types: dict[str, ClassDef] = {}
        self.agents: set[str] = set()
        self.nouns: dict[str, str | None] = {}
        self.verbs: dict[str, None] = {}
        self.matches = 0
        self.loops = 0

    # ------------------------------------------------------------ module

    def module(self, m: Module) -> str:
        self.collect(m)
        w = self.w
        w(f"# Generated from {self.filename} by the Mia compiler. Do not edit.")
        w(f"import {self.runtime} as rt")
        for s in m.body:
            if isinstance(s, Import):
                w(f"import {s.path}")

        for c in self.types.values():
            w()
            w()
            with w.block(f"class {c.name}({self.bases(c, c.bases, 'rt.Entity')}):"):
                w("pass")

        w()
        w()
        for name, type_name in self.nouns.items():
            typed = f", {type_name}" if type_name else ""
            w(f't_{name} = rt.noun("{name}"{typed})')
        for name in self.verbs:
            w(f't_{name} = rt.verb("{name}")')

        for s in m.body:
            match s:
                case AgentDef():
                    w()
                    w()
                    self.agent(s)
                case Import() | ClassDef():
                    pass
                case _:
                    raise MiaCompileError(s, f"{type(s).__name__} is not allowed at module level")
        return w.text()

    def collect(self, m: Module):
        contexts = set()
        for n in walk(m):
            match n:
                case ClassDef(name=name):
                    if name in self.types or name in RUNTIME_TYPES:
                        raise MiaCompileError(n, f"type {name} is already defined")
                    self.types[name] = n
                case AgentDef(name=name):
                    self.agents.add(name)
                case ContextDef(name=name):
                    contexts.add(name)
                case Clause(subj=None, verb="impasse", objs=[]):
                    pass
                case Clause(verb=verb):
                    self.verbs.setdefault(verb)
        for n in walk(m):
            if not isinstance(n, Name) or n.name in contexts:
                continue
            if n.type is None:
                self.nouns.setdefault(n.name, None)
                continue
            if n.type not in self.types:
                raise MiaCompileError(n, f"undeclared type {n.type}")
            known = self.nouns.get(n.name)
            if known and known != n.type:
                raise MiaCompileError(n, f"{n.name} is declared as both {known} and {n.type}")
            self.nouns[n.name] = n.type

    def type_name(self, node: Node, name: str) -> str:
        if name in self.types or name in self.agents:
            return name
        if name in RUNTIME_TYPES:
            return f"rt.{name}"
        raise MiaCompileError(node, f"undeclared type {name}")

    def bases(self, node: Node, bases: list[str], default: str) -> str:
        return ", ".join(self.type_name(node, b) for b in bases) or default

    def comment(self, node: Node) -> str:
        where = f"{self.filename}:{node.line}"
        if 0 < node.line <= len(self.source_lines):
            return f"# {where}  {self.source_lines[node.line - 1].strip()}"
        return f"# {where}"

    # ------------------------------------------------------------ agents

    def agent(self, a: AgentDef):
        w = self.w
        with w.block(f"class {a.name}({self.bases(a, a.bases, 'rt.Agent')}):"):
            w(self.comment(a))
            predicates = [s for s in a.body if isinstance(s, PredicateDef)]
            if predicates:
                items = ", ".join(f'"{p.name}": {self.predicate_type(p)}' for p in predicates)
                w(f"predicates = {{{items}}}")

            boot, rules, experts, names = None, [], [], set()
            for s in a.body:
                match s:
                    case PredicateDef() | ClassDef():
                        continue
                    case Def() | AgentDef():
                        if s.name in names:
                            raise MiaCompileError(s, f"{s.name} is already defined in {a.name}")
                        names.add(s.name)
                        w()
                        if isinstance(s, AgentDef):
                            self.agent(s)
                            experts.append(s.name)
                        else:
                            self.rule(s)
                            if s.name == a.name:
                                boot = s.name
                            else:
                                rules.append(s.name)
                    case _:
                        raise MiaCompileError(s, f"{type(s).__name__} is not allowed in an agent body")
            w()
            w(f"boot = {boot}")
            w(f"rules = {_tuple(rules)}")
            w(f"experts = {_tuple(experts)}")

    def predicate_type(self, p: PredicateDef) -> str:
        if p.type is None:
            return "object"
        if p.type in PY_TYPES:
            return p.type
        return self.type_name(p, p.type)

    # ------------------------------------------------------------ rules

    def rule(self, d: Def):
        w = self.w
        self.matches = 0
        self.loops = 0
        scope = _Scope()
        scope.contexts = {n.name for n in walk(d) if isinstance(n, ContextDef)}
        trigger, pattern = self.trigger(d)
        with w.block(f"class {d.name}(rt.Task):"):
            w(self.comment(d))
            w(f"trigger = {trigger}")
            w()
            self.bind(pattern, scope)
            w()
            self.resume(d, scope)

    def trigger(self, d: Def):
        t = d.trigger
        if t is None:
            return "None", None
        kind = MESSAGE_CLASSES[t.performative]
        match t.content:
            case Clause(subj=None, verb="impasse", objs=[], slots=[]) if t.performative is None:
                return "rt.IMPASSE", None
            case Clause(subj=None, verb=verb):
                raise MiaCompileError(t, f"'{verb}' needs a subject; write /{verb} for a perform goal")
            case Clause() as c:
                return f"rt.Trigger({kind}, rt.Belief, t_{c.verb})", c
            case Goal(kind=goal_kind, clause=c):
                return f"rt.Trigger({kind}, {GOAL_CLASSES[goal_kind]}, t_{c.verb})", c
            case Var(type=None) as v:
                return f"rt.Trigger({kind}, rt.Clause, None)", v
            case Var(type=type_name) as v if type_name in CLAUSE_TYPES:
                return f"rt.Trigger({kind}, rt.{type_name}, None)", v
            case _:
                raise MiaCompileError(t, "a trigger must be a clause, a goal, or a clause variable")

    def bind(self, pattern, scope: _Scope):
        w = self.w
        with w.block("def bind(self, msg):"):
            if pattern is not None and (
                isinstance(pattern, Var) or pattern.subj or pattern.objs or pattern.slots or pattern.bind
            ):
                w("_c = msg.clause")
                if isinstance(pattern, Var):
                    self.bind_trigger_value(pattern, "_c", scope)
                else:
                    if pattern.subj is not None:
                        self.bind_trigger_value(pattern.subj, "_c.subj", scope)
                    if len(pattern.objs) > 1:
                        raise MiaCompileError(pattern, "multiple objects in a trigger are not supported yet")
                    if pattern.objs:
                        self.bind_trigger_value(pattern.objs[0], "_c.obj", scope)
                    for slot in pattern.slots:
                        w(f'if "{slot.name}" not in _c.slots:')
                        w("    return False")
                        self.bind_trigger_value(slot.value, f'_c.slots["{slot.name}"]', scope)
                    if pattern.bind is not None:
                        self.bind_trigger_value(pattern.bind, "_c", scope)
            w("return True")

    def bind_trigger_value(self, term, expr: str, scope: _Scope):
        w = self.w
        match term:
            case Var(name="_"):
                pass
            case Var(name=name, type=type_name):
                if name in scope.task:
                    w(f"if {expr} != self.v_{name}:")
                    w("    return False")
                else:
                    scope.task[name] = None
                    w(f"self.v_{name} = {expr}")
                if type_name and type_name not in CLAUSE_TYPES:
                    w(f"if not isinstance(self.v_{name}, {self.type_name(term, type_name)}):")
                    w("    return False")
            case Name() | Literal() | Code():
                w(f"if {expr} != {self.term(term, scope)}:")
                w("    return False")
            case _:
                raise MiaCompileError(term, "unsupported term in a trigger")

    def resume(self, d: Def, scope: _Scope):
        w = self.w
        states: list[list] = [[]]
        for s in d.body:
            states[-1].append(s)
            if self.suspends(s):
                states.append([])
        with w.block("def resume(self, agent, result=None):"):
            if any(isinstance(n, Where) for n in walk(d)):
                w("ctx = agent.context")
            if len(states) == 1:
                self.state(states[0], 0, scope, last=True)
                return
            with w.block("match self.pc:"):
                for i, stmts in enumerate(states):
                    with w.block(f"case {i}:"):
                        self.state(stmts, i, scope, last=i == len(states) - 1)

    @staticmethod
    def suspends(s) -> bool:
        return isinstance(s, Message) and (s.propose or s.performative is None)

    def state(self, stmts: list, index: int, scope: _Scope, last: bool):
        w = self.w
        if index > 0:
            w("if not result.succeeded:")
            w("    return self.fail(agent)")
        for s in stmts:
            self.stmt(s, scope, "body", next_pc=index + 1)
        if last and not (stmts and isinstance(stmts[-1], TERMINATORS)):
            w("return self.succeed(agent)")

    # ------------------------------------------------------------ statements

    def stmt(self, s, scope: _Scope, mode: str, next_pc: int | None = None):
        w = self.w
        match s:
            case Where():
                self.where(s, scope)
            case ContextDef():
                self.context(s, scope)
            case Message():
                self.message(s, scope, mode, next_pc)
            case Return(value=None):
                w("return self.return_(agent)")
            case Return(value=value):
                w(f"return self.return_(agent, {self.term(value, scope)})")
            case Succeed():
                w("return self.succeed(agent)")
            case Fail():
                w("return self.fail(agent)")
            case Throw():
                w("return self.throw(agent)")
            case Halt():
                w("return agent.halt()")
            case Pass():
                if mode != "body":  # a rule body always ends in a return
                    w("pass")
            case Snippet(text=text):
                w(self.code(s, text, scope))
            case _:
                raise MiaCompileError(s, f"{type(s).__name__} is not allowed in a rule body")

    def block(self, stmts: list, scope: _Scope):
        for s in stmts:
            self.stmt(s, scope, "branch")

    def message(self, s: Message, scope: _Scope, mode: str, next_pc: int | None):
        w = self.w
        if s.paragraph:
            if s.propose or s.performative is not Performative.ASSERT:
                raise MiaCompileError(s, "only an assert (+) can have a paragraph in a rule body")
            self.paragraph(s, scope, lambda c: w(f"agent.post(rt.Assert({c}))"))
            return

        msg = f"{MESSAGE_CLASSES[s.performative]}({self.content(s.content, scope)})"
        if s.propose:
            call = f"agent.propose({msg}"
        elif s.performative is None:
            call = f"agent.post({msg}"
        else:
            w(f"agent.post({msg})")
            return

        if mode == "body":
            w(f"self.pc = {next_pc}")
            w(f"return {call}, self)")
        else:
            w(f"{call})")

    def paragraph(self, s: Message, scope: _Scope, sink):
        match s.content:
            case Name() | Var():
                subj = self.term(s.content, scope)
            case Clause() | Goal():
                self.w(f"_h = {self.content(s.content, scope)}")
                sink("_h")
                subj = "_h"
            case _:
                raise MiaCompileError(s, "a paragraph needs a noun, variable, clause, or goal as its head")
        for p in s.paragraph:
            sink(self.clause("rt.Belief", subj, p, scope))

    def context(self, s: ContextDef, scope: _Scope):
        w = self.w
        w("_k = rt.Context()")
        sink = lambda c: w(f"_k.add({c})")
        for entry in s.body:
            if not isinstance(entry, Message) or entry.propose or entry.performative not in (
                None,
                Performative.ASSERT,
            ):
                raise MiaCompileError(entry, "a context can only hold facts and goals")
            if entry.paragraph:
                self.paragraph(entry, scope, sink)
            elif isinstance(entry.content, (Clause, Goal)):
                sink(self.content(entry.content, scope))
            elif not isinstance(entry.content, Name):
                raise MiaCompileError(entry, "a context entry must be a fact or a goal")
        w(f"self.c_{s.name} = _k")

    # ------------------------------------------------------------ where

    def where(self, s: Where, scope: _Scope):
        w = self.w
        m = f"_m{self.matches}"
        self.matches += 1
        w(f"{m} = []")

        inner = scope.child()
        bound: list[str] = []
        opened = sum(self.condition(c, inner, bound) for c in s.conditions)
        w(_tuple_append(m, [f"v_{name}" for name in bound]))
        w.depth -= opened

        for branch in s.branches:
            match branch.outcome:
                case Outcome.EACH:
                    target = _tuple([f"v_{name}" for name in bound]) if bound else "_"
                    with w.block(f"for {target} in {m}:"):
                        self.block(branch.body, scope.child(bound))
                case Outcome.ANY:
                    with w.block(f"if {m}:"):
                        self.block(branch.body, scope)
                case Outcome.NONE:
                    with w.block(f"if not {m}:"):
                        self.block(branch.body, scope)

    def condition(self, cond, scope: _Scope, bound: list[str]) -> int:
        """Emit one condition and return how many blocks it opened."""
        w = self.w
        match cond:
            case Match(clause=c):
                self.check_pattern(c, negated=False)
                positions = [("subj", c.subj)] + ([("obj", c.objs[0])] if c.objs else [])
                free = [self.is_free(t, scope) for _, t in positions]
                args = [
                    "rt.ANY" if is_free or _is_blank(t) else self.term(t, scope)
                    for (_, t), is_free in zip(positions, free)
                ]
                obj_arg = args[1] if c.objs else "rt.ANY"
                loop = f"_c{self.loops}"
                self.loops += 1
                w(f"for {loop} in ctx.find(rt.Belief, {args[0]}, t_{c.verb}, {obj_arg}):")
                w.depth += 1
                opened = 1
                for (attr, t), is_free in zip(positions, free):
                    opened += self.bind_pattern(t, f"{loop}.{attr}", scope, bound, constrained=not is_free)
                for slot in c.slots:
                    w(f'if "{slot.name}" in {loop}.slots:')
                    w.depth += 1
                    opened += 1
                    opened += self.bind_pattern(
                        slot.value, f'{loop}.slots["{slot.name}"]', scope, bound, constrained=False
                    )
                return opened
            case NoMatch(clause=c):
                self.check_pattern(c, negated=True)
                subj = self.pattern_arg(c.subj, scope)
                obj = self.pattern_arg(c.objs[0], scope) if c.objs else "rt.ANY"
                w(f"if not ctx.exists(rt.Belief, {subj}, t_{c.verb}, {obj}):")
            case Compare(left=left, op=op, right=right):
                w(f"if {self.term(left, scope)} {op} {self.term(right, scope)}:")
            case Filter(code=code):
                w(f"if {self.term(code, scope)}:")
            case _:
                raise MiaCompileError(cond, f"unsupported condition {type(cond).__name__}")
        w.depth += 1
        return 1

    @staticmethod
    def check_pattern(c: Clause, negated: bool):
        if c.subj is None:
            raise MiaCompileError(c, f"'{c.verb}' needs a subject in a condition")
        if len(c.objs) > 1:
            raise MiaCompileError(c, "multiple objects in a condition are not supported yet")
        if c.bind is not None:
            raise MiaCompileError(c, "-> bindings are only allowed in triggers")
        if negated and (c.slots or any(isinstance(t, Var) and t.type for t in [c.subj, *c.objs])):
            raise MiaCompileError(c, "slots and types in negated conditions are not supported yet")

    @staticmethod
    def is_free(term, scope: _Scope) -> bool:
        return isinstance(term, Var) and term.name != "_" and not scope.bound(term.name)

    def pattern_arg(self, term, scope: _Scope) -> str:
        if _is_blank(term) or self.is_free(term, scope):
            return "rt.ANY"
        return self.term(term, scope)

    def bind_pattern(self, term, expr: str, scope: _Scope, bound: list[str], constrained: bool) -> int:
        w = self.w
        opened = 0
        match term:
            case Var(name="_"):
                return 0
            case Var(name=name, type=type_name):
                if scope.bound(name):
                    if not constrained:
                        w(f"if {expr} == {self.term(term, scope)}:")
                        w.depth += 1
                        opened += 1
                else:
                    w(f"v_{name} = {expr}")
                    scope.locals.add(name)
                    bound.append(name)
                if type_name:
                    w(f"if isinstance({self.term(term, scope)}, {self.type_name(term, type_name)}):")
                    w.depth += 1
                    opened += 1
            case _:
                if not constrained:
                    w(f"if {expr} == {self.term(term, scope)}:")
                    w.depth += 1
                    opened += 1
        return opened

    # ------------------------------------------------------------ expressions

    def content(self, c, scope: _Scope) -> str:
        match c:
            case Goal(kind=GoalKind.PERFORM, clause=clause):
                return self.clause("rt.Perform", "rt.SELF", clause, scope)
            case Goal(kind=kind, clause=clause):
                if clause.subj is None:
                    raise MiaCompileError(c, f"{kind.value}{clause.verb} needs a subject")
                return self.clause(GOAL_CLASSES[kind], self.term(clause.subj, scope), clause, scope)
            case Clause(subj=None, verb=verb):
                raise MiaCompileError(c, f"'{verb}' needs a subject; write /{verb} for a perform goal")
            case Clause():
                return self.clause("rt.Belief", self.term(c.subj, scope), c, scope)
            case _:
                return self.term(c, scope)

    def clause(self, cls: str, subj: str, c: Clause, scope: _Scope) -> str:
        if c.bind is not None:
            raise MiaCompileError(c, "-> bindings are only allowed in triggers")
        args = [subj, f"t_{c.verb}"]
        if len(c.objs) > 1:
            obj = _tuple([self.term(t, scope) for t in c.objs])
        elif c.objs:
            obj = self.term(c.objs[0], scope)
        else:
            obj = None
        if c.slots:
            slots = ", ".join(f'"{s.name}": {self.term(s.value, scope)}' for s in c.slots)
            args += [obj or "None", f"{{{slots}}}"]
        elif obj is not None:
            args.append(obj)
        return f"{cls}({', '.join(args)})"

    def term(self, t, scope: _Scope) -> str:
        match t:
            case Var(name="_"):
                raise MiaCompileError(t, "$_ can only be used in patterns")
            case Var(name=name):
                if name in scope.locals:
                    return f"v_{name}"
                if name in scope.task:
                    return f"self.v_{name}"
                raise MiaCompileError(t, f"${name} is not bound here")
            case Name(name=name):
                return f"self.c_{name}" if name in scope.contexts else f"t_{name}"
            case Literal(value=value):
                return repr(value)
            case Code(text=text):
                return f"({self.code(t, text, scope)})"
            case Clause() | Goal():
                return self.content(t, scope)
            case _:
                raise MiaCompileError(t, f"unsupported term {type(t).__name__}")

    def code(self, node: Node, text: str, scope: _Scope) -> str:
        return _DOLLAR.sub(lambda m: self.term(Var(m.group(1), line=node.line), scope), text)


def _tuple_append(target: str, items: list[str]) -> str:
    return f"{target}.append({_tuple(items) if items else '()'})"
