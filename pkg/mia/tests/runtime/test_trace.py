"""Tracing and the run command."""
import pytest

import crunge.mia.runtime as rt
from crunge.mia.cli import main
from crunge.mia.load import agent_classes, load_source
from tests.samples import sample, sample_path


@pytest.fixture(scope="module")
def blox():
    return load_source(sample("blox.mia"), "blox_mia", "blox.mia")


def traced_run(agent_class):
    sink = rt.ListSink()
    host = rt.AgentHost(agent_class, tracer=rt.Tracer(sink))
    assert host.run() is rt.Status.SUCCEEDED
    return host, sink.events


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
    host, events = traced_run(blox.BloxAgent)
    assert events[0]["event"] == "trace" and events[0]["agent"] == "BloxAgent"

    outer, inner = of(events, "agency")
    assert inner["agent"] == "BloxAgent.Blox" and inner["parent"] == outer["root"]
    assert of(events, "spawn")[0]["agent"] == inner["root"]

    # every non-root agent is announced by a fork before its state is recorded
    forks = {e["agent"]: e for e in of(events, "fork")}
    seen = set()
    for e in events:
        if e["event"] == "fork":
            seen.add(e["agent"])
        elif e["event"] == "state" and e["agent"] not in (outer["root"], inner["root"]):
            assert e["agent"] in seen

    # the root state lists the whole context; forks list only changes
    root_state = of(events, "state", agent=inner["root"])[0]
    assert {"Block1 onTop Table1", "@Block1 onTop Block2", "(@Block1 onTop Block2) status Active"} <= set(root_state["added"])
    assert root_state["removed"] == []

    # walk the solution back to the root through fork events
    solution = of(events, "solution", agency=inner["agency"])[0]
    path, agent = [], solution["agent"]
    while agent in forks:
        path.append(forks[agent]["proposal"])
        agent = forks[agent]["parent"]
    assert agent == inner["root"]
    assert path[::-1] == ["@Block2 onTop Block3", "@Block3 onTop Table1", "@Block2 onTop Block3", "@Block1 onTop Block2"]

    final = of(events, "state", agent=solution["agent"])[0]
    assert final["status"] == "SUCCEEDED" and final["cost"] == 4
    assert "Block1 onTop Block2" in final["added"]
    assert of(events, "result", agency=inner["agency"])[0]["expansions"] == 5


def test_untraced_agents_emit_nothing(blox):
    host = rt.AgentHost(blox.BloxAgent)
    assert host.run() is rt.Status.SUCCEEDED
    assert host.agent.tracer is None and host.agent.id == 0


def test_run_command_writes_a_trace(tmp_path, capsys):
    out = tmp_path / "trip.miatrace"
    with sample_path("trip.mia") as program:
        assert main(["run", str(program), "--trace", str(out)]) == 0
    printed = capsys.readouterr().out
    assert "Go (cost 4):" in printed and "[Drive]" in printed

    events = rt.read_trace(out)
    assert events[0]["event"] == "trace"
    assert [e["plan"] for e in of(events, "fork") if e["plan"]] == ["Walk", "Drive"]


def test_run_command_priority_option(tmp_path, capsys):
    try:
        with sample_path("trip.mia") as program:
            assert main(["run", str(program), "--priority", "breadth_first"]) == 0
        assert "Go (cost 11):" in capsys.readouterr().out
    finally:
        rt.Agent.priority = None


def test_agent_classes_lists_top_level_agents(blox):
    assert agent_classes(blox) == [blox.BloxAgent]
