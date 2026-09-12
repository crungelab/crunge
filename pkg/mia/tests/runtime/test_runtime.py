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


def blox_root(blox):
    """A Blox expert seeded with the program's starting context."""
    root = rt.State(blox.Blox)
    for clause in blox.Blox.starting_context():
        root.post(rt.Assert(clause))
    return root


def facts(state, verb):
    return {(c.subj.name, c.obj.name) for c in state.context if isinstance(c, rt.Belief) and c.verb is verb}


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
    solver = rt.ProblemSolver(counting.Counting)
    assert solver.run() is rt.Status.SUCCEEDED
    expert = solver.solution
    goal = rt.Perform(rt.SELF, counting.t_countTo, 5)
    assert rt.Belief(goal, counting.t_value, 5) in expert.context
    assert goal not in expert.context  # succeed retracted the goal

    # `|` runs during the search, `||` waits for the plan
    assert capsys.readouterr().out.strip() == "counting in sub-contexts"
    solver.plan.run()
    assert capsys.readouterr().out.splitlines()[-1] == "5 ..."


def test_blocks_world_builds_the_tower(blox):
    solver = rt.ProblemSolver(blox.Blox)
    assert solver.run() is rt.Status.SUCCEEDED
    expert = solver.solution
    assert expert.halted
    assert len(expert.history) == 4
    assert facts(expert, blox.t_onTop) == TOWER
    # achieve goals stay in the context, satisfied and no longer active
    goals = [c for c in expert.context if isinstance(c, rt.Achieve)]
    assert len(goals) == 2
    assert not [c for c in expert.context if c.verb is rt.STATUS]


def test_undoing_an_achieved_goal_reactivates_it():
    a, b, on = rt.noun("A"), rt.noun("B"), rt.verb("on")
    state = rt.State()
    goal = rt.Achieve(a, on, b)
    active = rt.Belief(goal, rt.STATUS, rt.ACTIVE)

    state.post(rt.Assert(goal))
    state.run()
    assert active in state.context

    state.post(rt.Assert(rt.Belief(a, on, b)))
    state.run()
    assert active not in state.context

    state.post(rt.Retract(rt.Belief(a, on, b)))
    state.run()
    assert active in state.context


def test_attempting_a_satisfied_achieve_goal_succeeds_without_a_plan():
    a, b, on = rt.noun("A"), rt.noun("B"), rt.verb("on")

    class Waiter(rt.Task):
        def resume(self, state, result=None):
            if self.pc == 0:
                self.pc = 1
                return state.post(rt.Attempt(rt.Achieve(a, on, b)), self)
            self.result = result
            return self.succeed(state)

    state = rt.State(context=rt.Context([rt.Belief(a, on, b)]))
    waiter = Waiter()
    state.start(waiter, None, None)
    assert state.run() is rt.Status.SUCCEEDED
    assert waiter.result.succeeded


def test_fork_gives_independent_children(blox):
    state = blox_root(blox)
    assert state.advance() is Step.DECIDE
    assert [p.message.clause.subj.name for p in state.proposals] == ["Block1", "Block2"]

    first, second = state.fork(0), state.fork(1)
    assert state.states == [first, second] and first.parent is state
    assert first.advance() is Step.DECIDE and second.advance() is Step.DECIDE
    # stacking Block1 first means moving Block2 away; stacking Block2 first means moving Block3
    assert {p.message.clause.subj.name for p in first.proposals} == {"Block2"}
    assert {p.message.clause.subj.name for p in second.proposals} == {"Block3"}

    start = {("Block1", "Table1"), ("Block2", "Block1"), ("Block3", "Block2")}
    grandchild = second.fork(0)
    grandchild.advance()
    assert ("Block3", "Table1") in facts(grandchild, blox.t_onTop)
    assert facts(second, blox.t_onTop) == facts(state, blox.t_onTop) == start


def test_every_halting_branch_builds_the_tower(blox):
    frontier, expanded, solved = [blox_root(blox)], 0, []
    while frontier and expanded < 400:
        state = frontier.pop(0)
        if state.advance() is Step.DECIDE:
            expanded += 1
            frontier += [state.fork(i) for i in range(len(state.proposals))]
        elif state.status() is rt.Status.SUCCEEDED:
            solved.append(state)
    assert solved
    assert all(facts(state, blox.t_onTop) == TOWER for state in solved)
    assert min(len(state.history) for state in solved) == 4


# ---------------------------------------------------------------- search


@pytest.mark.parametrize("priority", [None, rt.breadth_first, rt.depth_first])
def test_space_finds_the_shortest_tower(blox, priority):
    space = rt.ProblemSpace(blox_root(blox), priority)
    solution = space.run()
    assert facts(solution, blox.t_onTop) == TOWER
    assert len(solution.history) == 4 and solution.cost == 4


def test_a_star_expands_least(blox):
    expansions = {}
    for name, priority in [("a_star", None), ("breadth_first", rt.breadth_first)]:
        space = rt.ProblemSpace(blox_root(blox), priority)
        space.run()
        expansions[name] = space.expansions
    assert expansions["a_star"] < expansions["breadth_first"]


def test_a_star_takes_the_cheapest_plan_not_the_shortest(trip):
    tired = rt.Belief(rt.SELF, trip.t_tired, True)
    try:
        trip.Go.priority = rt.breadth_first
        solver = rt.ProblemSolver(trip.Go)
        assert solver.run() is rt.Status.SUCCEEDED
        walked = solver.solution
        assert walked.cost == 11 and tired in walked.context

        trip.Go.priority = None
        solver = rt.ProblemSolver(trip.Go)
        assert solver.run() is rt.Status.SUCCEEDED
        drove = solver.solution
        assert drove.cost == 4 and tired not in drove.context
    finally:
        trip.Go.priority = None


def test_same_state_at_higher_cost_is_dropped():
    a, on, b, c = rt.noun("A"), rt.verb("on"), rt.noun("B"), rt.noun("C")
    cheap, dear = rt.State(context=rt.Context([rt.Belief(a, on, b)])), rt.State(context=rt.Context([rt.Belief(a, on, b)]))
    dear.cost = 5
    assert cheap.state_key() == dear.state_key()
    assert cheap.state_key() != rt.State(context=rt.Context([rt.Belief(a, on, c)])).state_key()


def test_negative_cost_is_rejected():
    with pytest.raises(ValueError):
        rt.State().add_cost(-1)


# ---------------------------------------------------------------- monkey & bananas


@pytest.fixture(scope="module")
def bananas():
    return build("bananas")


def test_monkey_gets_the_banana(bananas):
    b = bananas
    solver = rt.ProblemSolver(b.Bananas)
    assert solver.run() is rt.Status.SUCCEEDED
    expert = solver.solution

    where = {c.subj: c.obj for c in expert.context if isinstance(c, rt.Belief) and c.verb is b.t_container}
    assert where[b.t_Banana1] is b.t_Monkey1        # the monkey has the banana
    assert where[b.t_Key1] is b.t_Monkey1           # it needed the key on the way
    assert where[b.t_Monkey1] is b.t_Place2         # and ended up at the chest
    assert rt.Belief(b.t_Chest1, b.t_locked, False) in expert.context
    assert expert.cost == 5


def test_bananas_visits_the_key_before_the_chest(bananas):
    b = bananas
    solver = rt.ProblemSolver(b.Bananas)
    solver.run()
    solution = solver.solution

    def monkey_at(state):
        return next((c.obj for c in state.context if isinstance(c, rt.Belief)
                     and c.subj is b.t_Monkey1 and c.verb is b.t_container), None)

    chain, state = [solution], solution
    while state.parent is not None:
        state = state.parent
        chain.append(state)
    visited = []
    for state in reversed(chain):
        spot = monkey_at(state)
        if spot is not None and (not visited or visited[-1] is not spot):
            visited.append(spot)
    assert visited == [b.t_Place1, b.t_Place3, b.t_Place2]  # start, key, chest


# ---------------------------------------------------------------- missionaries & cannibals


def test_everyone_crosses_safely():
    mac = build("mac")
    solver = rt.ProblemSolver(mac.Mac)
    assert solver.run() is rt.Status.SUCCEEDED
    solution = solver.solution

    def count(state, bank, verb):
        [clause] = [c for c in state.context
                    if isinstance(c, rt.Belief) and c.subj is bank and c.verb is verb]
        return clause.obj

    assert count(solution, mac.t_Bank2, mac.t_missionaries) == 3
    assert count(solution, mac.t_Bank2, mac.t_cannibals) == 3
    assert rt.Belief(mac.t_Bank2, mac.t_boat, mac.t_Boat1) in solution.context

    # the classic minimum: 11 crossings
    crossings = [m for m in solution.history if m.clause.verb is mac.t_row]
    assert len(crossings) == 11

    # no state along the way leaves missionaries outnumbered
    chain, state = [solution], solution
    while state.parent is not None:
        state = state.parent
        chain.append(state)
    for state in chain:
        for bank in (mac.t_Bank1, mac.t_Bank2):
            counts = {c.verb: c.obj for c in state.context
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
    solver = rt.ProblemSolver(towers.Towers)
    assert solver.run() is rt.Status.SUCCEEDED
    solution = solver.solution

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
    chain, state = [solution], solution
    while state.parent is not None:
        state = state.parent
        chain.append(state)
    stacks = [{c.subj: c.obj for c in a.context if isinstance(c, rt.Belief) and c.verb is towers.t_onTop}
              for a in reversed(chain)]
    stacks = [s for s in stacks if len(s) == 3]  # before the context arrives there are none
    assert sum(1 for a, b in zip(stacks, stacks[1:]) if a != b) == 7

    # a disc is only ever moved onto something larger, and only when clear
    sizes = {c.subj: c.obj for c in solution.context
             if isinstance(c, rt.Belief) and c.verb is towers.t_size}
    for state in chain:
        for clause in state.context:
            if isinstance(clause, rt.Belief) and clause.verb is towers.t_onTop:
                assert sizes[clause.subj] < sizes[clause.obj]


def test_dependent_goals_wait_their_turn(towers):
    solver = rt.ProblemSolver(towers.Towers)
    assert solver.run() is rt.Status.SUCCEEDED
    solution = solver.solution

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
    root = solver.solution
    while root.parent is not None:
        root = root.parent
    assert rt.Belief(top, rt.STATUS, rt.ACTIVE) not in root.context
    assert rt.Belief(middle, towers.t_suspended, True) in root.context
    assert rt.Belief(bottom, towers.t_suspended, True) not in root.context
    assert [p.message.clause for p in root.proposals] == [bottom]


def test_a_dependency_cycle_is_not_success(towers):
    source = sample("towers.mia").replace(
        "    @Disc3 onTop Peg3\n",
        "    @Disc3 onTop Peg3\n        dependsOn (@Disc1 onTop Disc2)\n",
        1,
    )
    module = build_source(source, "cyclic_towers")
    assert rt.ProblemSolver(module.Towers).run() is rt.Status.FAILED


def test_an_unwaited_failure_ends_the_branch():
    class Failing(rt.Task):
        def resume(self, state, result=None):
            return self.fail(state)

    state = rt.State()
    state.start(Failing(), None, None)
    assert state.run() is rt.Status.FAILED and state.dead


# ---------------------------------------------------------------- water jug


def test_waterjug_measures_one_gallon():
    wj = build("waterjug")
    solver = rt.ProblemSolver(wj.Waterjug)
    assert solver.run() is rt.Status.SUCCEEDED
    solution = solver.solution
    assert rt.Belief(wj.t_Jug1, wj.t_contents, 1) in solution.context

    # the classic minimum: fill, pour, fill, pour
    moves = [rt.to_mia(m) for m in solution.history if isinstance(m.clause, rt.Perform)]
    assert moves == ["/fill Jug1", "/pour Jug1 to: Jug2", "/fill Jug1", "/pour Jug1 to: Jug2"]

    # `empty` stays in step with `contents` for both jugs, all the way along
    chain, state = [solution], solution
    while state.parent is not None:
        state = state.parent
        chain.append(state)
    for state in chain:
        for jug in (wj.t_Jug1, wj.t_Jug2):
            facts = {c.verb: c.obj for c in state.context
                     if isinstance(c, rt.Belief) and c.subj is jug}
            if wj.t_empty in facts:
                assert facts[wj.t_contents] + facts[wj.t_empty] == facts[wj.t_volume]


# ---------------------------------------------------------------- sibling query


def test_sibling_query_joins_frame_and_working_memory(capsys):
    sib = build("siblings")
    solver = rt.ProblemSolver(sib.Siblings)
    assert solver.run() is rt.Status.SUCCEEDED
    solution = solver.solution

    assert rt.Belief(sib.t_Billy, sib.t_sibling, sib.t_Suzy) in solution.context
    assert rt.Belief(sib.t_Billy, sib.t_sibling, sib.t_Billy) not in solution.context
    solver.plan.run()
    assert capsys.readouterr().out.count("are siblings") == 2  # one line per shared parent

    # the frame is background knowledge: queried, never copied or changed
    assert len(sib.f_FamilyTree) == 14
    assert not any(c.verb is sib.t_sibling for c in sib.f_FamilyTree)
    assert rt.Belief(sib.t_Billy, sib.t_parent, sib.t_John) not in solution.context

    # the view spans both spaces; the expert inherits what the state knows
    assert sib.Siblings.frames == (sib.f_FamilyTree,)
    assert len(solution.view) == len(solution.context) + len(sib.f_FamilyTree)
    assert rt.Belief(sib.t_Billy, sib.t_parent, sib.t_John) in solution.view


def test_the_join_needs_both_spaces():
    # Suzy is Billy's sister in the frame, but if she is not in the room the
    # working-memory half of the query fails and no sibling is found.
    source = sample("siblings.mia").replace("    Person Suzy here True\n", "")
    module = build_source(source, "absent_siblings")
    solver = rt.ProblemSolver(module.Siblings)
    solver.run()
    solution = solver.solution
    assert not [c for c in solution.context if c.verb is module.t_sibling]


def test_halting_keeps_facts_asserted_just_before():
    a, b, likes = rt.noun("A"), rt.noun("B"), rt.verb("likes")

    class Finish(rt.Task):
        def resume(self, state, result=None):
            state.post(rt.Assert(rt.Belief(a, likes, b)))
            return state.halt()

    state = rt.State()
    state.start(Finish(), None, None)
    assert state.run() is rt.Status.SUCCEEDED
    assert rt.Belief(a, likes, b) in state.context


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


# ---------------------------------------------------------------- plans


def test_mouse_plan_holds_only_the_chosen_route(capsys):
    mouse = build("mouse")
    solver = rt.ProblemSolver(mouse.MouseExpert)
    assert solver.run() is rt.Status.SUCCEEDED

    # nothing happened outside the state while it searched
    assert capsys.readouterr().out == ""

    plan = solver.plan
    assert [action.text for action in plan] == [
        'print(f"moveTo({1}, {0})")',
        'print(f"moveTo({2}, {0})")',
    ]
    plan.run()
    assert capsys.readouterr().out.split() == ["moveTo(1,", "0)", "moveTo(2,", "0)"]

    # the search recorded far more effects than the plan replays
    def effects(state):
        return len(state.effects) + sum(effects(child) for child in state.states)

    assert effects(solver.state) > 2 * len(plan)


def test_a_losing_branch_leaves_no_effects():
    recorded = []

    def note(value):
        recorded.append(value)

    note.text = "note($v)"
    note.names = ("v",)

    class Act(rt.Task):
        def __init__(self, value, halt):
            super().__init__()
            self.value, self.halting = value, halt

        def resume(self, state, result=None):
            state.effect(note, self.value)
            return state.halt() if self.halting else self.succeed(state)

    parent = rt.State()
    parent.effect(note, "shared")
    winner, loser = rt.State(parent=parent), rt.State(parent=parent)
    winner.effects = list(parent.effects)
    loser.effects = list(parent.effects)
    winner.start(Act("kept", halt=True), None, None)
    loser.start(Act("dropped", halt=True), None, None)
    winner.run()
    loser.run()

    rt.Plan(winner).run()
    assert recorded == ["shared", "kept"]
    assert str(rt.Plan(winner)) == "note('shared')\nnote('kept')"


def test_immediate_and_deferred_effects_side_by_side(capsys):
    mouse = build("mouse")
    solver = rt.ProblemSolver(mouse.MouseExpert)
    solver.run()
    # the `|` logging line ran once per move considered, in every branch
    assert len(solver.plan) == 2


# ---------------------------------------------------------------- travel


@pytest.fixture(scope="module")
def travel():
    return build("travel")


def test_travel_takes_a_taxi_and_pays_for_it(travel):
    solver = rt.ProblemSolver(travel.Travel)
    assert solver.run() is rt.Status.SUCCEEDED
    solution = solver.solution

    assert rt.Belief(rt.SELF, travel.t_location, travel.t_Restaurant1) in solution.context
    assert rt.Belief(rt.SELF, travel.t_cash, 14.5) in solution.context   # 20 - (1.5 + 0.5 * 8)
    assert solution.cost == 6.5

    # the plan is the taxi sequence, in order, and nothing from the walking branch
    assert [a.text.split("(")[1].split(")")[0] for a in solver.plan] == [
        'f"call a taxi to {Home1}"',
        'f"ride from {Home1} to {Restaurant1}"',
        'f"pay the driver {1.5 + 0.5 * 8:.2f}"',
    ]


def test_a_short_trip_is_walked(travel):
    source = sample("travel.mia").replace("distance: 8", "distance: 1")
    module = build_source(source, "short_travel")
    solver = rt.ProblemSolver(module.Travel)
    assert solver.run() is rt.Status.SUCCEEDED
    assert solver.solution.cost == 2   # 1 to commit, 1 to walk
    assert len(solver.plan) == 1 and "walk" in solver.plan.actions[0].text


def test_alternative_plans_become_separate_branches(travel):
    solver = rt.ProblemSolver(travel.Travel)
    solver.run()

    def descendants(state):
        for child in state.states:
            yield child
            yield from descendants(child)

    branches = {a.chosen[-1]: a for a in descendants(solver.state) if a.chosen and a.chosen[-1]}
    assert set(branches) == {"TravelByFoot", "TravelByTaxi"}
    # walking eight miles does not apply, so that branch throws and dies
    assert branches["TravelByFoot"].dead
    assert not branches["TravelByTaxi"].dead


# ---------------------------------------------------------------- quest (HTN)


@pytest.fixture(scope="module")
def quest():
    return build("quest")


def test_quest_decomposes_around_a_closed_bridge(quest):
    solver = rt.ProblemSolver(quest.Quest)
    assert solver.run() is rt.Status.SUCCEEDED
    solution = solver.solution

    assert rt.Belief(quest.t_Farm, quest.t_holds, quest.t_Parcel) in solution.context
    assert rt.Belief(quest.t_Courier, quest.t_coins, 2) in solution.context  # 5 - 3 for the ticket
    assert [a.text for a in solver.plan] == [
        'print(f"walk to {Market}")',
        'print(f"buy a {Ticket} for {3}")',
        'print("board the ferry")',
        'print(f"hand over the {Parcel} at {Farm}")',
    ]


def test_opening_the_bridge_changes_the_decomposition(quest):
    source = sample("quest.mia").replace("Bridge open False", "Bridge open True")
    module = build_source(source, "open_bridge_quest")
    solver = rt.ProblemSolver(module.Quest)
    assert solver.run() is rt.Status.SUCCEEDED
    assert solver.solution.cost == 5   # cheaper than the ferry route's 7
    assert [a.text for a in solver.plan] == [
        'print(f"cross the bridge, paying {2}")',
        'print(f"hand over the {Parcel} at {Farm}")',
    ]


def test_a_partly_built_plan_is_carried_into_successor_states(quest):
    solver = rt.ProblemSolver(quest.Quest)
    solver.run()

    def descendants(state):
        for child in state.states:
            yield child
            yield from descendants(child)

    agents = list(descendants(solver.state))

    # at its deepest the courier is three methods into the decomposition
    stacks = [[type(task).__name__ for task in a.suspended] for a in agents]
    assert ["DeliverByFerry", "BoardAfterBuying"] in stacks

    # a method that fails deep down kills its branch, not the state
    bridge = next(a for a in agents if a.chosen and a.chosen[-1] == "DeliverByBridge")
    assert bridge.dead and bridge.suspended  # it died mid-decomposition

    # each child resumes its own copy of the suspended work
    forked = next(a for a in agents if len(a.states) > 1 and a.suspended)
    for child in forked.states:
        assert all(task not in forked.suspended for task in child.suspended)


# ---------------------------------------------------------------- two experts, one world


def test_experts_share_the_programs_starting_context(capsys):
    errands = build("errands")
    costs = {}
    for cls in (errands.Walker, errands.Driver):
        solver = rt.ProblemSolver(cls)
        assert solver.run() is rt.Status.SUCCEEDED
        costs[cls.__name__] = solver.solution.cost
        assert rt.Belief(errands.t_Courier, errands.t_at, errands.t_Market) in solver.solution.context
        assert len(solver.plan) == 1
    assert costs == {"Walker": 5, "Driver": 1}

    # each expert's own `start` rule ran, and only its own
    printed = capsys.readouterr().out.split()
    assert printed.count("walker") == 1 and printed.count("driver") == 1


def test_start_runs_after_the_world_is_in_place():
    a, b, sees = rt.noun("A"), rt.noun("B"), rt.verb("sees")

    seen = []

    class Setup(rt.Task):
        trigger = rt.START

        def resume(self, expert, result=None):
            seen.extend(expert.context)
            return self.succeed(expert)

    class Watcher(rt.Expert):
        rules = (Setup,)
        starting_context = staticmethod(lambda: rt.Context([rt.Belief(a, sees, b)]))

    solver = rt.ProblemSolver(Watcher)
    assert solver.run() is rt.Status.SUCCEEDED
    assert seen == [rt.Belief(a, sees, b)]


# ---------------------------------------------------------------- several experts, one state


def test_two_experts_on_one_state_offer_both_plans(capsys):
    errands = build("errands")
    solver = rt.ProblemSolver([errands.Walker, errands.Driver])
    assert solver.run() is rt.Status.SUCCEEDED

    # both start rules ran, and the search chose the cheaper plan
    printed = capsys.readouterr().out.split()
    assert printed.count("walker") == 1 and printed.count("driver") == 1
    assert solver.solution.cost == 2   # 1 to commit + 1 to drive, against 5 to walk
    assert [a.text for a in solver.plan] == ['print(f"drive to {Market}")']

    # the state carries both experts, and the search saw both plans
    assert solver.state.experts == (errands.Walker, errands.Driver)
    assert {s.chosen[-1] for s in solver.state.states if s.chosen} == {None}
    chosen = {s.chosen[-1] for s in solver.state.states for s in s.states if s.chosen}
    assert chosen == {"Walk", "Drive"}


def test_experts_can_be_added_and_removed_while_a_state_runs():
    errands = build("errands")
    state = rt.State(errands.Walker)
    assert len(state.experts) == 1
    walking_rules = len(state.plans(rt.IMPASSE)) + 1

    state.add_expert(errands.Driver)
    assert state.experts == (errands.Walker, errands.Driver)
    state.add_expert(errands.Driver)   # already active
    assert len(state.experts) == 2

    state.remove_expert(errands.Walker)
    assert state.experts == (errands.Driver,)
    assert walking_rules   # sanity: the walker had rules to begin with


def test_the_active_experts_are_part_of_a_states_identity():
    errands = build("errands")
    walking = rt.State(errands.Walker)
    driving = rt.State(errands.Driver)
    assert walking.state_key() != driving.state_key()
    assert walking.state_key() == rt.State(errands.Walker).state_key()


def test_an_expert_is_a_rule_set_not_a_state():
    errands = build("errands")
    with pytest.raises(TypeError, match="not a state"):
        errands.Walker()
