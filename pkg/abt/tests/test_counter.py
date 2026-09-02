import pytest

from crunge.abt.run.act import *
from crunge.abt.run.task import Task, Runner, Status

from . import step_until


@pytest.fixture
def runner():
    """The Runner is a singleton, so reset its state between tests."""
    r = Runner()
    r.cancel_all()
    r.time = 0.0
    r.steps = 0
    yield r
    r.cancel_all()


def drain(runner, dt=0.0, max_steps=200):
    steps = 0
    while runner.queue:
        assert steps < max_steps, f"queue did not drain in {max_steps} steps"
        runner.step(dt)
        steps += 1
    return steps


def recorder(log, name, status=None, sleeps=0):
    async def fn(task, msg):
        log.append(name)
        for _ in range(sleeps):
            await task.sleep()
        if status is not None:
            return status
        return

    return fn


#
# COUNT
#
def test_count_visible_through_parent(runner):
    """The original test's shape -- a child reads the count off its parent."""
    counts = []

    with counter(1, 11) as top:
        with action() as a:
            async def fn(task, msg):
                counts.append(task.parent.count)

            a.use(fn)

    top.run(max_steps=400)

    assert counts == list(range(1, 11))
    assert top.status is Status.SUCCESS


def test_count_starts_at_start(runner):
    counts = []

    with counter(5, 8) as c:
        with action() as a:
            async def fn(task, msg):
                counts.append(c.count)

            a.use(fn)

    c.run(max_steps=200)

    assert counts == [5, 6, 7]


def test_count_stop_is_exclusive(runner):
    counts = []

    with counter(0, 3) as c:
        with action() as a:
            async def fn(task, msg):
                counts.append(c.count)

            a.use(fn)

    c.run(max_steps=200)

    assert counts == [0, 1, 2]
    assert c.count == 2, "count retains the last value after finishing"


def test_negative_range_runs_nothing(runner):
    log = []

    with counter(5, 2) as c:
        with action() as a:
            a.use(recorder(log, "never"))

    c.run(max_steps=200)

    assert log == []
    assert c.status is Status.SUCCESS


def test_single_iteration(runner):
    log = []

    with counter(1, 2) as c:
        with action() as a:
            a.use(recorder(log, "once"))

    c.run(max_steps=200)

    assert log == ["once"]
    assert c.status is Status.SUCCESS


def test_counter_with_no_children_succeeds(runner):
    with counter(1, 5) as c:
        pass

    c.run(max_steps=200)

    assert c.status is Status.SUCCESS


#
# ITERATION AND RESET
#
def test_child_reruns_each_iteration(runner):
    """Each iteration needs a fresh coroutine frame, not a re-await of a
    finished task."""
    entries = []

    with counter(1, 4) as c:
        with action() as a:
            async def fn(task, msg):
                entries.append(task.status)

            a.use(fn)

    c.run(max_steps=200)

    assert len(entries) == 3
    assert all(s is Status.RUNNING for s in entries)


def test_child_state_is_cleared_between_iterations(runner):
    """reset() clears result, so a child cannot see its own last return."""
    seen = []

    with counter(1, 4) as c:
        with action() as a:
            async def fn(task, msg):
                seen.append(task.result)
                return "payload"

            a.use(fn)

    c.run(max_steps=200)

    assert seen == [None, None, None]


def test_child_with_sleeps_completes_each_iteration(runner):
    log = []

    with counter(1, 4) as c:
        with action() as a:
            a.use(recorder(log, "tick", sleeps=2))

    c.run(max_steps=400)

    assert log == ["tick", "tick", "tick"]


def test_nested_sequence_restarts_each_iteration(runner):
    """The subtree, not just the immediate child, must be reset."""
    log = []

    with counter(1, 4) as c:
        with sequence():
            with action() as a:
                a.use(recorder(log, "a"))
            with action() as a:
                a.use(recorder(log, "b"))

    c.run(max_steps=400)

    assert log == ["a", "b"] * 3
    assert c.status is Status.SUCCESS


def test_nested_counters(runner):
    pairs = []

    with counter(1, 3) as outer:
        with counter(10, 12) as inner:
            with action() as a:
                async def fn(task, msg):
                    pairs.append((outer.count, inner.count))

                a.use(fn)

    outer.run(max_steps=400)

    assert pairs == [(1, 10), (1, 11), (2, 10), (2, 11)]


#
# FAILURE
#
def test_failure_stops_counting(runner):
    counts = []

    with counter(1, 11) as c:
        with action() as a:
            async def fn(task, msg):
                if c.count > 3:
                    return task.fail()
                counts.append(c.count)

            a.use(fn)

    c.run(max_steps=400)

    assert counts == [1, 2, 3]
    assert c.status is Status.FAILURE
    assert c.count == 4, "count reflects the iteration that failed"


def test_failure_on_second_child_stops_counting(runner):
    log = []

    with counter(1, 5) as c:
        with action() as a:
            a.use(recorder(log, "first"))
        with action() as a:
            async def fn(task, msg):
                log.append("second")
                if c.count >= 2:
                    return task.fail()

            a.use(fn)

    c.run(max_steps=400)

    assert log == ["first", "second", "first", "second"]
    assert c.status is Status.FAILURE


def test_raising_child_stops_counting(runner):
    counts = []

    with counter(1, 11) as c:
        with action() as a:
            async def fn(task, msg):
                if c.count > 2:
                    raise ValueError("boom")
                counts.append(c.count)

            a.use(fn)

    c.run(max_steps=400)

    assert counts == [1, 2]
    assert c.status is Status.FAILURE


#
# CANCELLATION
#
def test_cancel_mid_count(runner):
    log = []

    with counter(1, 100) as c:
        with action() as a:
            a.use(recorder(log, "tick", sleeps=1))

    runner.schedule(c)
    step_until(runner, lambda: len(log) >= 2, max_steps=40)

    c.cancel()
    before = len(log)
    drain(runner)

    assert len(log) == before
    assert c.status is Status.CANCELLED


def test_cancel_all_tears_down_a_counter(runner):
    log = []

    with counter(1, 100) as c:
        with action() as a:
            a.use(recorder(log, "tick", sleeps=1))

    runner.schedule(c)
    step_until(runner, lambda: len(log) >= 1, max_steps=40)

    runner.cancel_all()

    assert runner.queue == []
    assert c.status.done