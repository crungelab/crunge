"""Tracing and the run command."""
import pytest

import crunge.mia.runtime as rt
from crunge.mia.cli import main
from crunge.mia.load import expert_classes, load_source
from tests.samples import sample, sample_path


@pytest.fixture(scope="module")
def blox():
    return load_source(sample("blox.mia"), "blox_mia", "blox.mia")


def traced_run(agent_class):
    sink = rt.ListSink()
    solver = rt.ProblemSolver(agent_class, tracer=rt.Tracer(sink))
    assert solver.run() is rt.Status.SUCCEEDED
    return solver, sink.events


def of(events, kind, **match):
    return [e for e in events if e["event"] == kind and all(e.get(k) == v for k, v in match.items())]


def test_to_mia():
    b1, on, b2, count_to = rt.noun("Block1"), rt.verb("onTop"), rt.noun("Block2"), rt.verb("countTo")
    goal = rt.Perform(rt.SELF, count_to, 5)
    assert rt.to_mia(rt.Achieve(b1, on, b2)) == "@Block1 onTop Block2"
    assert rt.to_mia(rt.Attempt(rt.Perform(rt.SELF, rt.verb("stack"), b1, {"on": b2}))) == "/stack Block1 on: Block2"
    assert rt.to_mia(rt.Assert(rt.Belief(goal, rt.verb("value"), 0))) == "+ (/countTo 5) value 0"
    assert rt.to_mia(rt.Modify(rt.Belief(b1, rt.verb("isClear"), True))) == "-+ Block1 isClear True"
    assert rt.to_mia(rt.IMPASSE) == "impasse"


def test_trace_describes_the_search(blox):
    solver, events = traced_run(blox.Blox)
    assert events[0]["event"] == "trace" and events[0]["expert"] == "Blox"

    [space] = of(events, "space")
    assert space["expert"] == "Blox" and space["parent"] is None
    assert of(events, "spawn") == []   # one expert, no sub-space

    # every non-root state is announced by a fork before its status is recorded
    forks = {e["state"]: e for e in of(events, "fork")}
    seen = set()
    for e in events:
        if e["event"] == "fork":
            seen.add(e["state"])
        elif e["event"] == "status" and e["state"] != space["root"]:
            assert e["state"] in seen

    # the root state lists the whole context; forks list only changes
    root_status = of(events, "status", state=space["root"])[0]
    assert {"Block1 onTop Table1", "@Block1 onTop Block2", "(@Block1 onTop Block2) status Active"} <= set(root_status["added"])
    assert root_status["removed"] == []

    # walk the solution back to the root through fork events
    solution = of(events, "solution", space=space["space"])[0]
    path, state = [], solution["state"]
    while state in forks:
        path.append(forks[state]["proposal"])
        state = forks[state]["parent"]
    assert state == space["root"]
    assert path[::-1] == ["@Block2 onTop Block3", "@Block3 onTop Table1", "@Block2 onTop Block3", "@Block1 onTop Block2"]

    final = of(events, "status", state=solution["state"])[0]
    assert final["status"] == "SUCCEEDED" and final["cost"] == 4
    assert "Block1 onTop Block2" in final["added"]
    assert of(events, "result", space=space["space"])[0]["expansions"] == 5


def test_untraced_agents_emit_nothing(blox):
    solver = rt.ProblemSolver(blox.Blox)
    assert solver.run() is rt.Status.SUCCEEDED
    assert solver.state.tracer is None and solver.state.id == 0


def test_run_command_writes_a_trace(tmp_path, capsys):
    out = tmp_path / "trip.miatrace"
    with sample_path("trip.mia") as program:
        assert main(["run", str(program), "--trace", str(out)]) == 0
    printed = capsys.readouterr().out
    assert "Go: SUCCEEDED (cost 4)" in printed and "[Drive]" in printed

    events = rt.read_trace(out)
    assert events[0]["event"] == "trace"
    assert [e["plan"] for e in of(events, "fork") if e["plan"]] == ["Walk", "Drive"]


def test_run_command_priority_option(tmp_path, capsys):
    try:
        with sample_path("trip.mia") as program:
            assert main(["run", str(program), "--priority", "breadth_first"]) == 0
        assert "Go: SUCCEEDED (cost 11)" in capsys.readouterr().out
    finally:
        rt.Expert.priority = None


def test_expert_classes_lists_top_level_experts(blox):
    assert expert_classes(blox) == [blox.Blox]


def test_run_activates_every_expert_by_default(capsys):
    with sample_path("errands.mia") as program:
        assert main(["run", str(program)]) == 0
    printed = capsys.readouterr().out
    assert "walker ready" in printed and "driver ready" in printed
    assert "Walker + Driver: SUCCEEDED (cost 2)" in printed

    with sample_path("errands.mia") as program:
        assert main(["run", str(program), "--expert", "Walker"]) == 0
    printed = capsys.readouterr().out
    assert "driver ready" not in printed
    assert "Walker: SUCCEEDED (cost 5)" in printed
