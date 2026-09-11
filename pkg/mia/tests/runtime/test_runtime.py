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
    return build_source(sample(f"{name}.mia"), name)


def build_source(source, name):
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


# ---------------------------------------------------------------- monkey & bananas


@pytest.fixture(scope="module")
def bananas():
    return build("bananas")


def test_monkey_gets_the_banana(bananas):
    b = bananas
    host = rt.AgentHost(b.BananasAgent)
    assert host.run() is rt.Status.SUCCEEDED
    expert = host.solution.agents[0].solution

    where = {c.subj: c.obj for c in expert.context if isinstance(c, rt.Belief) and c.verb is b.t_container}
    assert where[b.t_Banana1] is b.t_Monkey1        # the monkey has the banana
    assert where[b.t_Key1] is b.t_Monkey1           # it needed the key on the way
    assert where[b.t_Monkey1] is b.t_Place2         # and ended up at the chest
    assert rt.Belief(b.t_Chest1, b.t_locked, False) in expert.context
    assert expert.cost == 5


def test_bananas_visits_the_key_before_the_chest(bananas):
    b = bananas
    host = rt.AgentHost(b.BananasAgent)
    host.run()
    solution = host.solution.agents[0].solution

    def monkey_at(agent):
        return next((c.obj for c in agent.context if isinstance(c, rt.Belief)
                     and c.subj is b.t_Monkey1 and c.verb is b.t_container), None)

    chain, agent = [solution], solution
    while agent.parent is not None:
        agent = agent.parent
        chain.append(agent)
    visited = []
    for agent in reversed(chain):
        spot = monkey_at(agent)
        if spot is not None and (not visited or visited[-1] is not spot):
            visited.append(spot)
    assert visited == [b.t_Place1, b.t_Place3, b.t_Place2]  # start, key, chest


# ---------------------------------------------------------------- missionaries & cannibals


def test_everyone_crosses_safely():
    mac = build("mac")
    host = rt.AgentHost(mac.MacAgent)
    assert host.run() is rt.Status.SUCCEEDED
    solution = host.solution.agents[0].solution

    def count(agent, bank, verb):
        [clause] = [c for c in agent.context
                    if isinstance(c, rt.Belief) and c.subj is bank and c.verb is verb]
        return clause.obj

    assert count(solution, mac.t_Bank2, mac.t_missionaries) == 3
    assert count(solution, mac.t_Bank2, mac.t_cannibals) == 3
    assert rt.Belief(mac.t_Bank2, mac.t_boat, mac.t_Boat1) in solution.context

    # the classic minimum: 11 crossings
    crossings = [m for m in solution.history if m.clause.verb is mac.t_row]
    assert len(crossings) == 11

    # no state along the way leaves missionaries outnumbered
    chain, agent = [solution], solution
    while agent.parent is not None:
        agent = agent.parent
        chain.append(agent)
    for agent in chain:
        for bank in (mac.t_Bank1, mac.t_Bank2):
            counts = {c.verb: c.obj for c in agent.context
                      if isinstance(c, rt.Belief) and c.subj is bank}
            missionaries = counts.get(mac.t_missionaries)
            cannibals = counts.get(mac.t_cannibals)
            if missionaries is None or cannibals is None:
                continue  # mid-move: the pair is updated one clause at a time
            assert missionaries == 0 or missionaries >= cannibals


# ---------------------------------------------------------------- towers of hanoi


@pytest.fixture(scope="module")
def towers():
    return build("towers")


def test_towers_moves_the_stack(towers):
    host = rt.AgentHost(towers.TowersAgent)
    assert host.run() is rt.Status.SUCCEEDED
    solution = host.solution.agents[0].solution

    stack = {c.subj: c.obj for c in solution.context
             if isinstance(c, rt.Belief) and c.verb is towers.t_onTop}
    assert stack == {
        towers.t_Disc1: towers.t_Disc2,
        towers.t_Disc2: towers.t_Disc3,
        towers.t_Disc3: towers.t_Peg3,
    }
    assert all(c.obj is towers.t_Peg3 for c in solution.context
               if isinstance(c, rt.Belief) and c.verb is towers.t_at
               and isinstance(c.subj, towers.Disc))

    # the classic minimum: 7 disc moves
    chain, agent = [solution], solution
    while agent.parent is not None:
        agent = agent.parent
        chain.append(agent)
    stacks = [{c.subj: c.obj for c in a.context if isinstance(c, rt.Belief) and c.verb is towers.t_onTop}
              for a in reversed(chain)]
    stacks = [s for s in stacks if len(s) == 3]  # before the context arrives there are none
    assert sum(1 for a, b in zip(stacks, stacks[1:]) if a != b) == 7

    # a disc is only ever moved onto something larger, and only when clear
    sizes = {c.subj: c.obj for c in solution.context
             if isinstance(c, rt.Belief) and c.verb is towers.t_size}
    for agent in chain:
        for clause in agent.context:
            if isinstance(clause, rt.Belief) and clause.verb is towers.t_onTop:
                assert sizes[clause.subj] < sizes[clause.obj]


def test_dependent_goals_wait_their_turn(towers):
    host = rt.AgentHost(towers.TowersAgent)
    assert host.run() is rt.Status.SUCCEEDED
    solution = host.solution.agents[0].solution

    top = rt.Achieve(towers.t_Disc1, towers.t_onTop, towers.t_Disc2)
    middle = rt.Achieve(towers.t_Disc2, towers.t_onTop, towers.t_Disc3)
    bottom = rt.Achieve(towers.t_Disc3, towers.t_onTop, towers.t_Peg3)

    # dependencies are elaborated both ways, and transitively
    assert rt.Belief(middle, towers.t_hasDependent, top) in solution.context
    assert rt.Belief(top, towers.t_indirectlyDependsOn, bottom) in solution.context

    # nothing is left suspended once every goal is achieved
    assert not [c for c in solution.context if c.verb is towers.t_suspended]

    # at the start Disc1 is already on Disc2, so that goal is not active;
    # the middle goal waits on the bottom one, leaving one thing to work on
    root = host.solution.agents[0]
    assert rt.Belief(top, rt.STATUS, rt.ACTIVE) not in root.context
    assert rt.Belief(middle, towers.t_suspended, True) in root.context
    assert rt.Belief(bottom, towers.t_suspended, True) not in root.context
    assert [p.message.clause for p in root.proposals] == [bottom]


def test_a_dependency_cycle_is_not_success(towers):
    source = sample("towers.mia").replace(
        "            @Disc3 onTop Peg3\n",
        "            @Disc3 onTop Peg3\n                dependsOn (@Disc1 onTop Disc2)\n",
        1,
    )
    module = build_source(source, "cyclic_towers")
    assert rt.AgentHost(module.TowersAgent).run() is rt.Status.FAILED


def test_an_unwaited_failure_ends_the_branch():
    class Failing(rt.Task):
        def resume(self, agent, result=None):
            return self.fail(agent)

    agent = rt.Agent()
    agent.start(Failing(), None, None)
    assert agent.run() is rt.Status.FAILED and agent.dead


# ---------------------------------------------------------------- water jug


def test_waterjug_measures_one_gallon():
    wj = build("waterjug")
    host = rt.AgentHost(wj.WaterjugAgent)
    assert host.run() is rt.Status.SUCCEEDED
    solution = host.solution.agents[0].solution
    assert rt.Belief(wj.t_Jug1, wj.t_contents, 1) in solution.context

    # the classic minimum: fill, pour, fill, pour
    moves = [rt.to_mia(m) for m in solution.history if isinstance(m.clause, rt.Perform)]
    assert moves == ["/fill Jug1", "/pour Jug1 to: Jug2", "/fill Jug1", "/pour Jug1 to: Jug2"]

    # `empty` stays in step with `contents` for both jugs, all the way along
    chain, agent = [solution], solution
    while agent.parent is not None:
        agent = agent.parent
        chain.append(agent)
    for agent in chain:
        for jug in (wj.t_Jug1, wj.t_Jug2):
            facts = {c.verb: c.obj for c in agent.context
                     if isinstance(c, rt.Belief) and c.subj is jug}
            if wj.t_empty in facts:
                assert facts[wj.t_contents] + facts[wj.t_empty] == facts[wj.t_volume]


# ---------------------------------------------------------------- sibling query


def test_sibling_query_joins_frame_and_working_memory(capsys):
    sib = build("siblings")
    host = rt.AgentHost(sib.SiblingAgent)
    assert host.run() is rt.Status.SUCCEEDED
    solution = host.solution.agents[0].solution

    assert rt.Belief(sib.t_Billy, sib.t_sibling, sib.t_Suzy) in solution.context
    assert rt.Belief(sib.t_Billy, sib.t_sibling, sib.t_Billy) not in solution.context
    assert capsys.readouterr().out.count("are siblings") == 2  # one line per shared parent

    # the frame is background knowledge: queried, never copied or changed
    assert len(sib.f_FamilyTree) == 14
    assert not any(c.verb is sib.t_sibling for c in sib.f_FamilyTree)
    assert rt.Belief(sib.t_Billy, sib.t_parent, sib.t_John) not in solution.context

    # the view spans both spaces; the expert inherits what the agent knows
    assert sib.SiblingAgent.Siblings.frames == (sib.f_FamilyTree,)
    assert len(solution.view) == len(solution.context) + len(sib.f_FamilyTree)
    assert rt.Belief(sib.t_Billy, sib.t_parent, sib.t_John) in solution.view


def test_the_join_needs_both_spaces():
    # Suzy is Billy's sister in the frame, but if she is not in the room the
    # working-memory half of the query fails and no sibling is found.
    source = sample("siblings.mia").replace("            Person Suzy here True\n", "")
    module = build_source(source, "absent_siblings")
    host = rt.AgentHost(module.SiblingAgent)
    host.run()
    solution = host.solution.agents[0].solution
    assert not [c for c in solution.context if c.verb is module.t_sibling]


def test_halting_keeps_facts_asserted_just_before():
    a, b, likes = rt.noun("A"), rt.noun("B"), rt.verb("likes")

    class Finish(rt.Task):
        def resume(self, agent, result=None):
            agent.post(rt.Assert(rt.Belief(a, likes, b)))
            return agent.halt()

    agent = rt.Agent()
    agent.start(Finish(), None, None)
    assert agent.run() is rt.Status.SUCCEEDED
    assert rt.Belief(a, likes, b) in agent.context


def test_view_merges_contexts_without_duplicates():
    a, b, likes = rt.noun("A"), rt.noun("B"), rt.verb("likes")
    shared = rt.Belief(a, likes, b)
    working = rt.Context([shared, rt.Belief(a, likes, a)])
    frame = rt.Context([shared, rt.Belief(b, likes, a)])
    view = rt.View((working, frame))

    assert len(view) == 3 and shared in view
    assert view.find(rt.Belief, a, likes, rt.ANY) == [shared, rt.Belief(a, likes, a)]
    assert view.find(rt.Belief, rt.ANY, likes, a) == [rt.Belief(a, likes, a), rt.Belief(b, likes, a)]
    assert view.exists(rt.Belief, b, likes, a) and not view.exists(rt.Belief, b, likes, b)
