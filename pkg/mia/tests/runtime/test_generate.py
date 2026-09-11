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


def test_blox_boot_builds_context_and_suspends(blox):
    agent = blox.BloxAgent()
    task = blox.BloxAgent.boot()
    assert task.bind(rt.Attempt(rt.Perform(rt.SELF, blox.t_bloxAgent)))
    assert task.resume(agent) == "SUSPENDED"

    ctx = task.c_BloxContext
    assert len(ctx.clauses) == 7
    assert rt.Belief(blox.t_Block1, blox.t_onTop, blox.t_Table1) in ctx.clauses
    assert isinstance(blox.t_Block3, blox.Block)
    assert agent.posts == [rt.Attempt(rt.Perform(rt.SELF, blox.t_blox, None, {"context": ctx}))]

    assert task.resume(agent, rt.Result(True)) == "SUCCEEDED"
    assert blox.BloxAgent.experts == (blox.BloxAgent.Blox,)


def test_stack_clears_first_and_returns(blox):
    agent = blox.BloxAgent.Blox(rt.Context([
        rt.Belief(blox.t_Block1, blox.t_onTop, blox.t_Table1),
        rt.Belief(blox.t_Block2, blox.t_onTop, blox.t_Block1),
    ]))
    task = blox.BloxAgent.Blox.Stack()
    assert task.bind(rt.Attempt(rt.Achieve(blox.t_Block1, blox.t_onTop, blox.t_Block2)))
    assert (task.v_x, task.v_y) == (blox.t_Block1, blox.t_Block2)

    assert task.resume(agent) == "RETURNED"
    assert agent.posts == [rt.Attempt(rt.Perform(rt.SELF, blox.t_clear, blox.t_Block1))]


def test_clear_proposes_every_clear_destination(blox):
    t = blox
    agent = t.BloxAgent.Blox(rt.Context([
        rt.Belief(t.t_Block1, t.t_beneath, t.t_Block2),
        rt.Belief(t.t_Table1, t.t_isClear, True),
        rt.Belief(t.t_Block2, t.t_isClear, True),
        rt.Belief(t.t_Block3, t.t_isClear, True),
    ]))
    task = t.BloxAgent.Blox.Clear()
    assert task.bind(rt.Attempt(rt.Perform(rt.SELF, t.t_clear, t.t_Block1)))
    assert task.resume(agent) == "SUCCEEDED"
    onto = lambda z: rt.Attempt(rt.Achieve(t.t_Block2, t.t_onTop, z))
    assert agent.proposals == [onto(t.t_Table1), onto(t.t_Block3)]


def test_typed_where_condition_checks_the_class(blox):
    t = blox
    rule = t.BloxAgent.Blox.OntopElab
    for target, expected in [(t.t_Block1, 2), (t.t_Table1, 1)]:
        agent = t.BloxAgent.Blox(rt.Context([
            rt.Belief(t.t_Block2, t.t_onTop, target),
            rt.Belief(target, t.t_isClear, True),
        ]))
        task = rule()
        assert task.bind(rt.Assert(rt.Belief(t.t_Block2, t.t_onTop, target)))
        task.resume(agent)
        assert len(agent.posts) == expected   # a Table stays clear


def test_tasks_copy_independently(blox):
    task = blox.BloxAgent.Blox.Stack()
    task.bind(rt.Attempt(rt.Achieve(blox.t_Block1, blox.t_onTop, blox.t_Block2)))
    clone = copy.copy(task)
    task.v_x = blox.t_Block3
    assert clone.v_x is blox.t_Block1


def test_counting(counting):
    t = counting
    boot = t.CountingAgent.boot()
    agent = t.CountingAgent()
    assert boot.resume(agent) == "SUSPENDED"
    goal, value = boot.c_CountingContext.clauses
    assert value == rt.Belief(goal, t.t_value, 0)

    counter = t.CountingAgent.Counting
    propose = counter.IncrementPropose()
    assert propose.bind(rt.Attempt(goal))
    agent = counter(boot.c_CountingContext)
    assert propose.resume(agent) == "RETURNED"
    assert agent.proposals == [rt.Attempt(rt.Perform(rt.SELF, t.t_increment, goal))]

    apply = counter.IncrementApply()
    assert apply.bind(rt.Attempt(rt.Perform(rt.SELF, t.t_increment, goal)))
    assert apply.resume(agent) == "SUCCEEDED"
    assert agent.posts == [rt.Modify(rt.Belief(goal, t.t_value, 1))]

    impasse = counter.Impasse()
    assert impasse.bind(None) and counter.Impasse.trigger is rt.IMPASSE
    assert impasse.resume(counter()) == "HALTED"


def test_errors_report_lines():
    with pytest.raises(MiaCompileError, match=r"line 3: \$y is not bound"):
        generate(parse("agent A\n    def B(/b $x)\n        + $x likes $y\n"))
    with pytest.raises(MiaCompileError, match="undeclared type Blok"):
        generate(parse("agent A\n    def A(/a)\n        context C\n            Blok B1 onTop T1\n"))


def test_cost_is_a_statement_and_still_a_verb():
    source = """agent A
    def B(/b)
        where
            Taxi1 cost $fare
            -->
            cost {$fare + 1}
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert "ctx.find(rt.Belief, t_Taxi1, t_cost, rt.ANY)" in code
    assert "agent.add_cost((v_fare + 1))" in code


def test_frames_are_module_level_and_shared():
    source = """class Person
frame Fam
    Person Billy parent John

agent A
    def A(/a $x)
        where in Fam
            $x parent $p
            -->
            pass
"""
    code = generate(parse(source), runtime="tests.fake_runtime")
    assert "f_Fam = _build_Fam()" in code
    assert "for _c0 in f_Fam.find(" in code
    assert "ctx = agent.context" not in code  # a frame-only rule never touches working memory


def test_unknown_frame_and_misplaced_frame_are_rejected():
    with pytest.raises(MiaCompileError, match="undeclared frame Nope"):
        generate(parse("agent A\n    def A(/a)\n        where in Nope\n            $x b $c\n            -->\n            pass\n"))
    with pytest.raises(MiaCompileError, match="belongs at module level"):
        generate(parse("agent A\n    frame F\n        X y Z\n    def A(/a)\n        pass\n"))


def test_knows_makes_queries_span_both_spaces():
    source = """class Person
frame Fam
    Person Billy parent John

agent A
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
    assert "ctx = agent.view" in code and "ctx = agent.context" not in code


def test_knows_an_undeclared_frame_is_rejected():
    with pytest.raises(MiaCompileError, match="undeclared frame Nope"):
        generate(parse("agent A\n    knows Nope\n    def A(/a)\n        pass\n"))
