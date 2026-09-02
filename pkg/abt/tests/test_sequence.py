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


def drain(runner, dt=0.0, max_steps=100):
    steps = 0
    while runner.queue:
        assert steps < max_steps, f"queue did not drain in {max_steps} steps"
        runner.step(dt)
        steps += 1
    return steps


def recorder(log, name, status=None, sleeps=0):
    """Build a coroutine body that records when it runs.

    `sleeps` yields control that many times before finishing, so ordering
    assertions still hold when steps interleave.
    """

    async def fn(task, msg):
        log.append(name)
        for _ in range(sleeps):
            await task.sleep()
        if status is not None:
            return status
        return

    return fn


#
# ORDERING
#
def test_children_run_in_order(runner):
    """The original test, with assertions."""
    log = []

    with sequence() as s:
        with action() as a:
            a.use(recorder(log, "Hi"))
        with action() as a:
            a.use(recorder(log, "Bye"))

    s.run()

    assert log == ["Hi", "Bye"]
    assert s.status is Status.SUCCESS


def test_children_are_serialized_not_concurrent(runner):
    """A sequence must await each child to completion before starting the
    next. With sleeps in the bodies, a concurrent implementation would
    interleave."""
    log = []

    with sequence() as s:
        with action() as a:
            a.use(recorder(log, "first", sleeps=2))
        with action() as a:
            a.use(recorder(log, "second", sleeps=2))

    s.run()

    assert log == ["first", "second"]


def test_empty_sequence_succeeds(runner):
    with sequence() as s:
        pass

    s.run()

    assert s.status is Status.SUCCESS


def test_single_child(runner):
    log = []

    with sequence() as s:
        with action() as a:
            a.use(recorder(log, "only"))

    s.run()

    assert log == ["only"]
    assert s.status is Status.SUCCESS


#
# FAILURE PROPAGATION
#
def test_failure_stops_the_sequence(runner):
    """The defining behaviour: a failed child aborts the rest."""
    log = []

    with sequence() as s:
        with action() as a:
            a.use(recorder(log, "first"))
        with action() as a:
            a.use(recorder(log, "second", status=Status.FAILURE))
        with action() as a:
            a.use(recorder(log, "third"))

    s.run()

    assert log == ["first", "second"]
    assert s.status is Status.FAILURE


def test_first_child_failure(runner):
    log = []

    with sequence() as s:
        with action() as a:
            a.use(recorder(log, "first", status=Status.FAILURE))
        with action() as a:
            a.use(recorder(log, "second"))

    s.run()

    assert log == ["first"]
    assert s.status is Status.FAILURE


def test_raising_child_fails_the_sequence(runner):
    """An exception is a failure, not a crash that takes out the batch."""
    log = []

    async def boom(task, msg):
        log.append("boom")
        raise ValueError("boom")

    with sequence() as s:
        with action() as a:
            a.use(boom)
        with action() as a:
            a.use(recorder(log, "after"))

    s.run()

    assert log == ["boom"]
    assert s.status is Status.FAILURE


#
# NESTING
#
def test_nested_sequences(runner):
    log = []

    with sequence() as outer:
        with action() as a:
            a.use(recorder(log, "a"))
        with sequence():
            with action() as a:
                a.use(recorder(log, "b"))
            with action() as a:
                a.use(recorder(log, "c"))
        with action() as a:
            a.use(recorder(log, "d"))

    outer.run()

    assert log == ["a", "b", "c", "d"]
    assert outer.status is Status.SUCCESS


def test_inner_failure_propagates_outward(runner):
    log = []

    with sequence() as outer:
        with action() as a:
            a.use(recorder(log, "a"))
        with sequence():
            with action() as a:
                a.use(recorder(log, "b", status=Status.FAILURE))
            with action() as a:
                a.use(recorder(log, "c"))
        with action() as a:
            a.use(recorder(log, "d"))

    outer.run()

    assert log == ["a", "b"]
    assert outer.status is Status.FAILURE


#
# CANCELLATION
#
def test_cancel_stops_a_running_sequence(runner):
    """Cancelling mid-run must not let the remaining children start."""
    log = []

    with sequence() as s:
        with action() as a:
            a.use(recorder(log, "first", sleeps=5))
        with action() as a:
            a.use(recorder(log, "second"))

    runner.schedule(s)
    step_until(runner, lambda: log == ["first"])

    s.cancel()
    drain(runner)

    assert log == ["first"]
    assert s.status is Status.CANCELLED


def test_cancelled_child_does_not_read_as_success(runner):
    """The concrete bug behind TS_SUCCESS = None: a sequence woken by a
    cancelled child would march on to the next step."""
    log = []

    with sequence() as s:
        with action() as first:
            first.use(recorder(log, "first", sleeps=5))
        with action() as a:
            a.use(recorder(log, "second"))

    runner.schedule(s)
    step_until(runner, lambda: log == ["first"])

    first.cancel()
    drain(runner)

    assert log == ["first"], "sequence continued past a cancelled child"
    assert s.status is not Status.SUCCESS


def test_cancel_all_tears_down_a_sequence(runner):
    log = []

    with sequence() as s:
        with action() as a:
            a.use(recorder(log, "first", sleeps=5))
        with action() as a:
            a.use(recorder(log, "second"))

    runner.schedule(s)
    step_until(runner, lambda: log == ["first"])

    runner.cancel_all()

    assert runner.queue == []
    assert s.status.done