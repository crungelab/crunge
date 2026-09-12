"""miascope's view logic: camera, scene, timeline, and inspector reports."""
import pytest

from crunge.miascope.camera import Camera
from crunge.miascope.inspector import report
from crunge.miascope.model import Phase
from crunge.miascope.scene import Scene
from crunge.miascope.timeline import Timeline, describe
from tests.traces import record


def measure(text):
    return 7.0 * len(text)


@pytest.fixture(scope="module")
def blox():
    solver, trace = record("blox.mia")
    return solver, trace, Scene(trace, measure)


# ---------------------------------------------------------------- camera


def test_camera_round_trip_and_zoom_about_a_point():
    camera = Camera(x=10, y=-5, zoom=2)
    assert camera.to_world(*camera.to_screen(3, 4)) == pytest.approx((3, 4))
    before = camera.to_world(200, 150)
    camera.zoom_at(200, 150, 1.5)
    assert camera.zoom == 3
    assert camera.to_world(200, 150) == pytest.approx(before)


def test_camera_pan_follows_the_drag():
    camera = Camera(zoom=2)
    world = camera.to_world(100, 100)
    camera.pan(20, -10)
    assert camera.to_screen(*world) == pytest.approx((120, 90))


def test_camera_fit_and_clamps():
    camera = Camera()
    camera.fit(0, 0, 2000, 500, width=1000, height=800)
    left, top, right, bottom = camera.visible(1000, 800)
    assert left <= 0 and right >= 2000 and top <= 0 and bottom >= 500
    camera.fit(0, 0, 10, 10, width=1000, height=800)
    assert camera.zoom == 1  # never magnifies a small tree
    camera.zoom_at(0, 0, 1e9)
    assert camera.zoom == camera.max_zoom


# ---------------------------------------------------------------- scene


def test_scene_boxes_edges_and_solution(blox):
    _, trace, scene = blox
    assert set(scene.boxes) == set(trace.nodes.values())
    assert len(scene.edges) == len(trace.nodes) - 1
    assert not any(e.spawn for e in scene.edges)   # one expert, so no sub-space

    space = trace.top
    assert set(trace.solution_path(space)) <= scene.solution
    assert space.root in scene.solution
    solution_edges = [e for e in scene.edges if e.solution]
    assert len(solution_edges) == len(trace.solution_path(space)) - 1   # 4 commits

    box = scene.boxes[space.root]
    assert box.right - box.left == measure("Blox") + 2 * scene.padding
    edge = next(e for e in scene.edges if e.parent is space.root)
    assert (edge.x0, edge.y0) == ((box.left + box.right) / 2, box.bottom)


def test_scene_visibility_follows_time(blox):
    _, trace, scene = blox
    expert = trace.top
    solution = expert.solution
    before = solution.created - 1
    assert solution not in {b.node for b, _ in scene.visible(before)}
    assert solution in {b.node for b, _ in scene.visible()}
    assert all(e.child is not solution for e in scene.visible_edges(before))

    box = scene.boxes[solution]
    cx, cy = (box.left + box.right) / 2, (box.top + box.bottom) / 2
    assert scene.hit(cx, cy) is solution
    assert scene.hit(cx, cy, before) is None
    assert scene.hit(box.right + 1000, cy) is None


def test_scene_culls_to_a_rectangle(blox):
    _, _, scene = blox
    left, top, right, bottom = scene.bounds
    assert len(list(scene.visible(rect=scene.bounds))) == len(scene.boxes)
    assert list(scene.visible(rect=(right + 10, top, right + 20, bottom))) == []


# ---------------------------------------------------------------- timeline


def test_timeline_playback():
    tl = Timeline(10, rate=4)
    assert tl.t == 9
    tl.toggle()  # at the end, play restarts from the beginning
    assert tl.playing and tl.t == 0
    tl.update(0.6)  # 2.4 events
    assert tl.t == 2
    tl.update(0.1)  # carry reaches 2.8
    assert tl.t == 2
    tl.update(10)
    assert tl.t == 9 and not tl.playing
    tl.seek(-5)
    assert tl.t == 0
    tl.step(100)
    assert tl.t == 9


def test_every_event_has_a_description(blox):
    _, trace, _ = blox
    texts = [describe(e) for e in trace.events]
    assert all(texts)
    assert any(t.startswith("fork state") and "@Block1 onTop Block2" in t for t in texts)


# ---------------------------------------------------------------- inspector


def test_report_marks_changes(blox):
    solver, trace, _ = blox
    expert = trace.top

    root = report(trace, expert.root)
    assert {row.change for row in root.context} == {"kept"}
    assert [p["message"] for p in root.proposals] == ["@Block1 onTop Block2", "@Block2 onTop Block3"]

    last = report(trace, expert.solution)
    changes = {row.clause: row.change for row in last.context}
    assert changes["Block1 onTop Block2"] == "added"
    assert changes["Block1 onTop Table1"] == "removed"
    assert changes["Block3 onTop Table1"] == "kept"
    assert dict(last.fields)["phase"] == "solution"
    assert dict(last.fields)["cost"] == "4"

    early = report(trace, expert.solution, expert.solution.created)
    assert dict(early.fields)["phase"] == Phase.RUNNING.value and early.context == []
    filtered = [row.clause for row in last.context if row.matches("ONTOP block2")]
    assert "Block1 onTop Block2" in filtered
    assert all("ontop block2" in clause.lower() for clause in filtered)
    assert len(filtered) < len(last.context)
