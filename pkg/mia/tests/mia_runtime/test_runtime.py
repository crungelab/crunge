"""Run the sample programs on the real runtime."""
import copy
import types

import pytest

import crunge.mia.runtime as rt
from crunge.mia.compile.codegen.generator import generate
from crunge.mia.compile.parse.parser import parse
from tests.samples import sample
from crunge.mia.runtime import Step


def build(name):
    source = sample(f"{name}.mia")
    module = types.ModuleType(f"{name}_mia")
    exec(compile(generate(parse(source), f"{name}.mia", source), f"{name}_mia.py", "exec"), module.__dict__)
    return module


@pytest.fixture(scope="module")
def blox():
    return build("blox")


@pytest.fixture(scope="module")
def counting():
    return build("counting")


@pytest.fixture(scope="module")
def trip():
    return build("trip")


def expert_solution(host):
    """The solved agent of the first expert spawned along the host's solution."""
    return host.solution.agents[0].solution


def blox_root(blox):
    """A Blox expert with BloxContext imported, ready to advance."""
    parent = blox.BloxAgent()
    boot = blox.BloxAgent.boot()
    boot.resume(parent)
    root = blox.BloxAgent.Blox()
    for clause in boot.c_BloxContext:
        root.post(rt.Assert(clause))
    return root


def facts(agent, verb):
    return {(c.subj.name, c.obj.name) for c in agent.context if isinstance(c, rt.Belief) and c.verb is verb}


TOWER = {("Block1", "Block2"), ("Block2", "Block3"), ("Block3", "Table1")}


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
    expert = expert_solution(host)
    goal = rt.Perform(rt.SELF, counting.t_countTo, 5)
    assert rt.Belief(goal, counting.t_value, 5) in expert.context
    assert goal not in expert.context  # succeed retracted the goal
    assert capsys.readouterr().out.splitlines()[-1] == "5 ..."


def test_blocks_world_builds_the_tower(blox):
    host = rt.AgentHost(blox.BloxAgent)
    assert host.run() is rt.Status.SUCCEEDED
    expert = expert_solution(host)
    assert expert.halted
    assert len(expert.history) == 4
    assert facts(expert, blox.t_onTop) == TOWER
    # achieve goals stay in the context, satisfied and no longer active
    goals = [c for c in expert.context if isinstance(c, rt.Achieve)]
    assert len(goals) == 2
    assert not [c for c in expert.context if c.verb is rt.STATUS]


def test_undoing_an_achieved_goal_reactivates_it():
    a, b, on = rt.noun("A"), rt.noun("B"), rt.verb("on")
    agent = rt.Agent()
    goal = rt.Achieve(a, on, b)
    active = rt.Belief(goal, rt.STATUS, rt.ACTIVE)

    agent.post(rt.Assert(goal))
    agent.run()
    assert active in agent.context

    agent.post(rt.Assert(rt.Belief(a, on, b)))
    agent.run()
    assert active not in agent.context

    agent.post(rt.Retract(rt.Belief(a, on, b)))
    agent.run()
    assert active in agent.context


def test_attempting_a_satisfied_achieve_goal_succeeds_without_a_plan():
    a, b, on = rt.noun("A"), rt.noun("B"), rt.verb("on")

    class Waiter(rt.Task):
        def resume(self, agent, result=None):
            if self.pc == 0:
                self.pc = 1
                return agent.post(rt.Attempt(rt.Achieve(a, on, b)), self)
            self.result = result
            return self.succeed(agent)

    agent = rt.Agent(rt.Context([rt.Belief(a, on, b)]))
    waiter = Waiter()
    agent.start(waiter, None, None)
    assert agent.run() is rt.Status.SUCCEEDED
    assert waiter.result.succeeded


def test_fork_gives_independent_children(blox):
    agent = blox_root(blox)
    assert agent.advance() is Step.DECIDE
    assert [p.message.clause.subj.name for p in agent.proposals] == ["Block1", "Block2"]

    first, second = agent.fork(0), agent.fork(1)
    assert agent.agents == [first, second] and first.parent is agent
    assert first.advance() is Step.DECIDE and second.advance() is Step.DECIDE
    # stacking Block1 first means moving Block2 away; stacking Block2 first means moving Block3
    assert {p.message.clause.subj.name for p in first.proposals} == {"Block2"}
    assert {p.message.clause.subj.name for p in second.proposals} == {"Block3"}

    start = {("Block1", "Table1"), ("Block2", "Block1"), ("Block3", "Block2")}
    grandchild = second.fork(0)
    grandchild.advance()
    assert ("Block3", "Table1") in facts(grandchild, blox.t_onTop)
    assert facts(second, blox.t_onTop) == facts(agent, blox.t_onTop) == start


def test_every_halting_branch_builds_the_tower(blox):
    frontier, expanded, solved = [blox_root(blox)], 0, []
    while frontier and expanded < 400:
        agent = frontier.pop(0)
        if agent.advance() is Step.DECIDE:
            expanded += 1
            frontier += [agent.fork(i) for i in range(len(agent.proposals))]
        elif agent.status() is rt.Status.SUCCEEDED:
            solved.append(agent)
    assert solved
    assert all(facts(agent, blox.t_onTop) == TOWER for agent in solved)
    assert min(len(agent.history) for agent in solved) == 4


# ---------------------------------------------------------------- search


@pytest.mark.parametrize("priority", [None, rt.breadth_first, rt.depth_first])
def test_agency_finds_the_shortest_tower(blox, priority):
    agency = rt.Agency(blox_root(blox), priority)
    solution = agency.run()
    assert facts(solution, blox.t_onTop) == TOWER
    assert len(solution.history) == 4 and solution.cost == 4


def test_a_star_expands_least(blox):
    expansions = {}
    for name, priority in [("a_star", None), ("breadth_first", rt.breadth_first)]:
        agency = rt.Agency(blox_root(blox), priority)
        agency.run()
        expansions[name] = agency.expansions
    assert expansions["a_star"] < expansions["breadth_first"]


def test_a_star_takes_the_cheapest_plan_not_the_shortest(trip):
    tired = rt.Belief(rt.SELF, trip.t_tired, True)
    try:
        trip.Trip.Go.priority = rt.breadth_first
        host = rt.AgentHost(trip.Trip)
        assert host.run() is rt.Status.SUCCEEDED
        walked = expert_solution(host)
        assert walked.cost == 11 and tired in walked.context

        trip.Trip.Go.priority = None
        host = rt.AgentHost(trip.Trip)
        assert host.run() is rt.Status.SUCCEEDED
        drove = expert_solution(host)
        assert drove.cost == 4 and tired not in drove.context
    finally:
        trip.Trip.Go.priority = None


def test_same_state_at_higher_cost_is_dropped():
    a, on, b, c = rt.noun("A"), rt.verb("on"), rt.noun("B"), rt.noun("C")
    cheap, dear = rt.Agent(rt.Context([rt.Belief(a, on, b)])), rt.Agent(rt.Context([rt.Belief(a, on, b)]))
    dear.cost = 5
    assert cheap.state_key() == dear.state_key()
    assert cheap.state_key() != rt.Agent(rt.Context([rt.Belief(a, on, c)])).state_key()


def test_negative_cost_is_rejected():
    with pytest.raises(ValueError):
        rt.Agent().add_cost(-1)
