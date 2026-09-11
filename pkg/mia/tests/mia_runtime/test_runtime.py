"""Run the sample programs on the real runtime."""
import copy
import types
from pathlib import Path

import pytest

import crunge.mia.runtime as rt
from crunge.mia.compile.codegen.generator import generate
from crunge.mia.compile.parse.parser import parse
from crunge.mia.runtime import Step

SAMPLES = Path(__file__).parent.parent / "samples"


def build(name):
    source = (SAMPLES / f"{name}.mia").read_text()
    module = types.ModuleType(f"{name}_mia")
    exec(compile(generate(parse(source), f"{name}.mia", source), f"{name}_mia.py", "exec"), module.__dict__)
    return module


@pytest.fixture(scope="module")
def blox():
    return build("blox")


@pytest.fixture(scope="module")
def counting():
    return build("counting")


def facts(agent, verb):
    return {(c.subj.name, c.obj.name) for c in agent.context if c.verb is verb}


# ---------------------------------------------------------------- data


def test_clauses_are_immutable_values():
    a, b = rt.noun("A"), rt.noun("B")
    on = rt.verb("on")
    c1 = rt.Perform(rt.SELF, on, a, {"to": b})
    c2 = rt.Perform(rt.SELF, on, a, {"to": b})
    assert c1 == c2 and hash(c1) == hash(c2)
    assert c1 != rt.Belief(rt.SELF, on, a, {"to": b})
    assert copy.deepcopy(c1) is c1 and rt.noun("A") is a
    with pytest.raises(AttributeError):
        c1.obj = b


def test_context_replace_and_find():
    a, value = rt.noun("A"), rt.verb("value")
    ctx = rt.Context([rt.Belief(a, value, 0)])
    assert ctx.replace(rt.Belief(a, value, 1)) == [rt.Belief(a, value, 0)]
    assert ctx.add(rt.Belief(a, value, 1)) and not ctx.add(rt.Belief(a, value, 1))
    assert ctx.find(rt.Belief, a, value, rt.ANY) == [rt.Belief(a, value, 1)]
    assert copy.deepcopy(ctx) is not ctx and len(copy.deepcopy(ctx)) == 1


# ---------------------------------------------------------------- programs


def test_counting_counts_to_five(counting, capsys):
    host = rt.AgentHost(counting.CountingAgent)
    assert host.run() is rt.Status.SUCCEEDED
    expert = host.agent.agents[0]
    goal = rt.Perform(rt.SELF, counting.t_countTo, 5)
    assert rt.Belief(goal, counting.t_value, 5) in expert.context
    assert goal not in expert.context  # succeed retracted the goal
    assert capsys.readouterr().out.splitlines()[-1] == "5 ..."


def test_blocks_world_halts(blox):
    host = rt.AgentHost(blox.BloxAgent)
    assert host.run() is rt.Status.SUCCEEDED
    expert = host.agent.agents[0]
    assert expert.halted
    assert not [c for c in expert.context if isinstance(c, rt.Goal)]


@pytest.mark.xfail(strict=True, reason="first-proposal commit undoes stack Block1 on Block2 after achieving it")
def test_blocks_world_builds_the_tower(blox):
    host = rt.AgentHost(blox.BloxAgent)
    host.run()
    assert facts(host.agent.agents[0], blox.t_onTop) == {
        ("Block1", "Block2"), ("Block2", "Block3"), ("Block3", "Table1"),
    }


def test_fork_gives_independent_children(blox):
    parent = blox.BloxAgent()
    boot = blox.BloxAgent.boot()
    assert boot.resume(parent) is rt.Status.SUSPENDED
    agent = blox.BloxAgent.Blox()
    for clause in boot.c_BloxContext:
        agent.post(rt.Assert(clause))

    assert agent.advance() is Step.DECIDE
    assert [p.message.clause.obj.name for p in agent.proposals] == ["Block1", "Block2"]

    first, second = agent.fork(0), agent.fork(1)
    assert agent.agents == [first, second] and first.parent is agent
    assert first.advance() is Step.DECIDE and second.advance() is Step.DECIDE
    # stacking Block1 first means moving Block2 away; stacking Block2 first means moving Block3
    assert {p.message.clause.obj.name for p in first.proposals} == {"Block2"}
    assert {p.message.clause.obj.name for p in second.proposals} == {"Block3"}

    start = {("Block1", "Table1"), ("Block2", "Block1"), ("Block3", "Block2")}
    grandchild = second.fork(0)
    grandchild.advance()
    assert ("Block3", "Table1") in facts(grandchild, blox.t_onTop)
    assert facts(second, blox.t_onTop) == facts(agent, blox.t_onTop) == start
