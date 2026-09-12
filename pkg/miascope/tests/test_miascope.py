"""miascope's trace model and tree layout."""
import json
import random
from importlib.resources import as_file

import pytest

import crunge.mia.runtime as rt
from crunge.miascope import Node, Phase, Trace, TraceError, tidy_tree
from tests.traces import ASSETS, record


@pytest.fixture(scope="module")
def blox():
    return record("blox.mia")


# ---------------------------------------------------------------- model


def test_spaces_and_states(blox):
    _, trace = blox
    assert trace.header["expert"] == "Blox"
    space = trace.top
    assert space.expert == "Blox" and space.spawner is None
    assert space.root.label == "Blox" and space.root.proposal is None
    assert space.expansions == 5 and not space.exhausted
    assert len(trace.spaces) == 1


def test_solution_path_and_outcomes(blox):
    _, trace = blox
    space = trace.top
    labels = [node.label for node in trace.solution_path(space)]
    assert labels == ["Blox", "@Block2 onTop Block3", "@Block3 onTop Table1", "@Block2 onTop Block3", "@Block1 onTop Block2"]

    phases = [node.phase() for node in space.nodes]
    assert phases.count(Phase.SOLUTION) == 1
    assert phases.count(Phase.EXPANDED) == 5
    assert phases.count(Phase.PRUNED) == sum(1 for e in trace.events if e["event"] == "prune")
    assert space.solution.cost == 4


def test_phase_over_time(blox):
    _, trace = blox
    space = trace.top
    node = space.solution
    assert node.phase(node.created - 1) is None
    assert node.phase(node.created) is Phase.RUNNING
    assert node.phase(node.reached) is Phase.QUEUED
    assert node.phase(node.resolved - 1) is Phase.QUEUED
    assert node.phase(node.resolved) is Phase.SOLUTION


def test_context_is_rebuilt_from_changes(blox):
    solver, trace = blox
    space = trace.top
    solved = solver.solution
    rebuilt = trace.context(space.solution)
    assert set(rebuilt) == {rt.to_mia(c) for c in solved.context}
    assert len(rebuilt) == len(solved.context)


def test_counting_context_reaches_five():
    _, trace = record("counting.mia")
    assert "(/countTo 5) value 5" in trace.context(trace.top.solution)


def test_load_from_file(tmp_path):
    from crunge.mia.cli import main

    out = tmp_path / "blox.miatrace"
    with as_file(ASSETS.joinpath("blox.mia")) as program:
        assert main(["run", str(program), "--trace", str(out)]) == 0
    trace = Trace.load(out)
    assert trace.top.expert == "Blox" and len(trace.nodes) == 9  # the root state plus 8 forks


def test_bad_traces_are_reported():
    with pytest.raises(TraceError, match="state 9"):
        Trace([{"event": "fork", "state": 10, "parent": 9, "proposal": "x"}])
    with pytest.raises(TraceError, match="top-level"):
        Trace([])


# ---------------------------------------------------------------- layout


class Tree:
    def __init__(self):
        self.children = []


def random_tree(rng, size):
    nodes = [Tree()]
    for _ in range(size - 1):
        parent = rng.choice(nodes[-30:] if rng.random() < 0.7 else nodes)
        child = Tree()
        parent.children.append(child)
        nodes.append(child)
    return nodes


def assert_tidy(nodes, children, pos, width, gap):
    for node in nodes:
        kids = children(node)
        if kids:
            assert pos[node].x == pytest.approx((pos[kids[0]].x + pos[kids[-1]].x) / 2)
            assert [pos[k].x for k in kids] == sorted(pos[k].x for k in kids)
    rows = {}
    for node in nodes:
        rows.setdefault(pos[node].y, []).append(node)
    for row in rows.values():
        row.sort(key=lambda n: pos[n].x)
        for a, b in zip(row, row[1:]):
            assert pos[b].x - pos[a].x >= (width(a) + width(b)) / 2 + gap - 1e-9


def test_layout_random_trees_with_varying_widths():
    rng = random.Random(42)
    for _ in range(200):
        nodes = random_tree(rng, rng.randint(1, 80))
        widths = {n: rng.choice([0.5, 1, 3, 8]) for n in nodes}
        pos = tidy_tree(nodes[0], lambda n: n.children, widths.__getitem__, gap=0.25, level=2)
        assert set(pos) == set(nodes)
        assert min(pos[n].x - widths[n] / 2 for n in nodes) == pytest.approx(0)
        assert_tidy(nodes, lambda n: n.children, pos, widths.__getitem__, 0.25)


def test_layout_handles_deep_trees():
    nodes = [Tree()]
    for _ in range(20_000):
        nodes[-1].children.append(Tree())
        nodes.append(nodes[-1].children[0])
    pos = tidy_tree(nodes[0], lambda n: n.children)
    assert pos[nodes[-1]].y == 20_000


def test_layout_of_a_trace(blox):
    _, trace = blox
    width = lambda node: len(node.label) * 0.6
    pos = tidy_tree(trace.top.root, Node.display_children, width, gap=1, level=3)
    assert len(pos) == len(trace.nodes)
    space = trace.top
    assert pos[space.root].y == 0 and pos[space.solution].y == 12
    assert_tidy(list(trace.nodes.values()), Node.display_children, pos, width, 1)


# ---------------------------------------------------------------- plans


def test_plan_is_readable_from_a_trace_alone():
    solver, trace = record("mouse.mia")
    space = trace.top
    actions = trace.plan(space.solution)
    assert actions == [action.text for action in solver.plan]

    # the top-level state's plan includes what the expert it spawned decided
    assert trace.plan(trace.top.solution) == actions

    # every branch's actions are in the trace; only the solution's are in the plan
    recorded = sum(len(node.actions) for node in trace.nodes.values())
    assert recorded > len(actions)


def test_sources_keep_the_live_plan_for_programs_only(tmp_path):
    from crunge.miascope.sources import load

    live = load("mouse.mia")
    assert live.runnable and [a.text for a in live.plan] == live.trace.plan(live.trace.top.solution)

    out = tmp_path / "mouse.miatrace"
    out.write_text("".join(json.dumps(e) + "\n" for e in live.trace.events), encoding="utf-8")
    from_disk = load(str(out))
    assert not from_disk.runnable  # the functions are gone, the text remains
    assert from_disk.trace.plan(from_disk.trace.top.solution) == live.trace.plan(live.trace.top.solution)
