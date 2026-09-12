"""Compile the sample .mia files to Python and run pieces of the output
against a fake runtime."""
import copy
import types

import pytest

from tests import fake_runtime as rt

from crunge.mia.compile.codegen.generator import MiaCompileError, generate
from crunge.mia.compile.parse.parser import parse
from tests.samples import sample


def build(name):
    source = sample(f"{name}.mia")
    code = generate(parse(source), f"{name}.mia", source, runtime="tests.fake_runtime")
    module = types.ModuleType(f"{name}_mia")
    exec(compile(code, f"{name}_mia.py", "exec"), module.__dict__)
    return module, code


@pytest.fixture(scope="module")
def blox():
    return build("blox")[0]


@pytest.fixture(scope="module")
def counting():
    return build("counting")[0]


def test_blox_starting_context(blox):
    context = blox.Blox.starting_context()
    assert len(context) == 7
    assert rt.Belief(blox.t_Block1, blox.t_onTop, blox.t_Table1) in context
    assert isinstance(blox.t_Block3, blox.Block)
    assert blox.Blox.entry is None   # nothing spawns it; the goals drive it


def test_stack_clears_first_and_returns(blox):
    state = blox.Blox(rt.Context([
        rt.Belief(blox.t_Block1, blox.t_onTop, blox.t_Table1),
        rt.Belief(blox.t_Block2, blox.t_onTop, blox.t_Block1),
    ]))
    task = blox.Blox.Stack()
    assert task.bind(rt.Attempt(rt.Achieve(blox.t_Block1, blox.t_onTop, blox.t_Block2)))
    assert (task.v_x, task.v_y) == (blox.t_Block1, blox.t_Block2)

    assert task.resume(state) == "RETURNED"
    assert state.posts == [rt.Attempt(rt.Perform(rt.SELF, blox.t_clear, blox.t_Block1))]


def test_clear_proposes_every_clear_destination(blox):
    t = blox
    state = t.Blox(rt.Context([
        rt.Belief(t.t_Block1, t.t_beneath, t.t_Block2),
        rt.Belief(t.t_Table1, t.t_isClear, True),
        rt.Belief(t.t_Block2, t.t_isClear, True),
        rt.Belief(t.t_Block3, t.t_isClear, True),
    ]))
    task = t.Blox.Clear()
    assert task.bind(rt.Attempt(rt.Perform(rt.SELF, t.t_clear, t.t_Block1)))
    assert task.resume(state) == "SUCCEEDED"
    onto = lambda z: rt.Attempt(rt.Achieve(t.t_Block2, t.t_onTop, z))
    assert state.proposals == [onto(t.t_Table1), onto(t.t_Block3)]


def test_typed_where_condition_checks_the_class(blox):
    t = blox
    rule = t.Blox.OntopElab
    for target, expected in [(t.t_Block1, 2), (t.t_Table1, 1)]:
        state = t.Blox(rt.Context([
            rt.Belief(t.t_Block2, t.t_onTop, target),
            rt.Belief(target, t.t_isClear, True),
        ]))
        task = rule()
        assert task.bind(rt.Assert(rt.Belief(t.t_Block2, t.t_onTop, target)))
        task.resume(state)
        assert len(state.posts) == expected   # a Table stays clear


def test_tasks_copy_independently(blox):
    task = blox.Blox.Stack()
    task.bind(rt.Attempt(rt.Achieve(blox.t_Block1, blox.t_onTop, blox.t_Block2)))
    clone = copy.copy(task)
    task.v_x = blox.t_Block3
    assert clone.v_x is blox.t_Block1


def test_counting(counting):
    t = counting
    context = t.Counting.starting_context()
    goal, value = context
    assert value == rt.Belief(goal, t.t_value, 0)

    propose = t.Counting.IncrementPropose()
    assert propose.bind(rt.Attempt(goal))
    expert = t.Counting(context)
    assert propose.resume(expert) == "RETURNED"
    assert expert.proposals == [rt.Attempt(rt.Perform(rt.SELF, t.t_increment, goal))]

    apply = t.Counting.IncrementApply()
    assert apply.bind(rt.Attempt(rt.Perform(rt.SELF, t.t_increment, goal)))
    assert apply.resume(expert) == "SUCCEEDED"
    assert expert.posts == [rt.Modify(rt.Belief(goal, t.t_value, 1))]
    [(function, args)] = expert.effects
    assert function.text == 'print($v1 + 1, "...")' and args == (0,)

    impasse = t.Counting.Impasse()
    assert impasse.bind(None) and t.Counting.Impasse.trigger is rt.IMPASSE
    assert impasse.resume(t.Counting()) == "HALTED"


def test_errors_report_lines():
    with pytest.raises(MiaCompileError, match=r"line 3: \$y is not bound"):
        generate(parse("expert A\n    def B(/b $x)\n        + $x likes $y\n"))
    with pytest.raises(MiaCompileError, match="undeclared type Blok"):
        generate(parse("expert A\n    def A(/a)\n        context C\n            Blok B1 onTop T1\n"))


def test_cost_is_a_statement_and_still_a_verb():
    source = """expert A
    def B(/b)
        where
            Taxi1 cost $fare
            -->
            cost {$fare + 1}
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert "ctx.find(rt.Belief, t_Taxi1, t_cost, rt.ANY)" in code
    assert "expert.add_cost((v_fare + 1))" in code


def test_frames_are_module_level_and_shared():
    source = """class Person
frame Fam
    Person Billy parent John

expert A
    def A(/a $x)
        where in Fam
            $x parent $p
            -->
            pass
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert "f_Fam = _build_Fam()" in code
    assert "for _c0 in f_Fam.find(" in code
    assert "ctx = expert.context" not in code  # a frame-only rule never touches working memory


def test_unknown_frame_and_misplaced_frame_are_rejected():
    with pytest.raises(MiaCompileError, match="undeclared frame Nope"):
        generate(parse("expert A\n    def A(/a)\n        where in Nope\n            $x b $c\n            -->\n            pass\n"))
    with pytest.raises(MiaCompileError, match="belongs at module level"):
        generate(parse("expert A\n    frame F\n        X y Z\n    def A(/a)\n        pass\n"))


def test_knows_makes_queries_span_both_spaces():
    source = """class Person
frame Fam
    Person Billy parent John

expert A
    knows Fam

    def A(/a $x)
        where
            $x parent $p
            -->
            pass

    expert E
        def E(/e)
            where
                $x parent $p
                -->
                pass
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert code.count("frames = (f_Fam,)") == 2   # the expert inherits it
    assert "ctx = expert.view" in code and "ctx = expert.context" not in code


def test_knows_an_undeclared_frame_is_rejected():
    with pytest.raises(MiaCompileError, match="undeclared frame Nope"):
        generate(parse("expert A\n    knows Nope\n    def A(/a)\n        pass\n"))


def test_immediate_and_deferred_snippets():
    source = """expert A
    def A(/a $p)
        where
            $p coordX $x
            -->
            | log(f"trying {$x}")
            || move_to($x)
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert 'log(f"trying {v_x}")' in code        # `|` runs where it is written
    assert "expert.effect(_effect_0, v_x)" in code  # `||` is recorded for the plan
    assert "def _effect_0(v_x):" in code
    assert "    move_to(v_x)" in code
    assert "_effect_0.names = ('x',)" in code


@pytest.mark.parametrize("bar", ["|", "||"])
def test_a_snippet_cannot_use_an_unbound_variable(bar):
    with pytest.raises(MiaCompileError, match=r"\$q is not bound"):
        generate(parse(f"expert A\n    def A(/a)\n        {bar} move_to($q)\n"), runtime="tests.fake_runtime")


def test_select_binds_for_the_rest_of_the_rule():
    source = """expert A
    def A(/a $to)
        select
            Self location $from
            !==>
            throw
        /go $from
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert "def _select0(ctx=expert.context):" in code
    assert "return (v_from,)" in code
    assert "return self.throw(expert)" in code
    assert "self.v_from, = _found" in code
    # the binding survives the suspension that follows
    assert "t_go, self.v_from" in code


def test_select_without_an_else_fails_when_nothing_matches():
    source = """expert A
    def A(/a)
        select
            Self location $from
        /go $from
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert "if _found is None:\n" in code and "return self.fail(expert)" in code


def test_a_select_else_body_must_end_the_rule():
    source = """expert A
    def A(/a)
        select
            Self location $from
            !==>
            /ask
        /go $from
"""
    with pytest.raises(MiaCompileError, match="must end the rule"):
        generate(parse(source), runtime="tests.fake_runtime")


def test_predicates_are_module_level_vocabulary():
    source = """class Block
predicate onTop(Block)
predicate isClear(bool)

expert Blox
    predicate scratch(int)

    def Note(+ $x onTop $y)
        pass
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert 'predicates = {"onTop": Block, "isClear": bool, "scratch": int}' in code


def test_start_and_impasse_are_signals():
    source = """expert A
    def Setup(start)
        pass

    def Stuck(impasse)
        pass
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert "trigger = rt.START" in code and "trigger = rt.IMPASSE" in code


def test_every_top_level_expert_starts_from_the_program_context():
    source = """class P
context W
    P Home

expert Walker
    def Go(/go)
        pass

expert Driver
    def Go(/go)
        pass
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert code.count("starting_context = staticmethod(_build_W)") == 2
