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
# COUNTER
#
def test_counter_runs_child_once_per_count(runner):
    log = []

    with counter(1, 4) as c:
        with action() as a:
            a.use(recorder(log, "tick"))

    c.run(max_steps=200)

    assert log == ["tick", "tick", "tick"]
    assert c.status is Status.SUCCESS


def test_counter_exposes_current_count(runner):
    counts = []

    with counter(1, 4) as c:
        with action() as a:
            async def fn(task, msg):
                counts.append(c.count)

            a.use(fn)

    c.run(max_steps=200)

    assert counts == [1, 2, 3]


def test_counter_stops_on_child_failure(runner):
    """The original test's shape: fail once the count passes a threshold."""
    log = []

    with counter(1, 11) as c:
        with action() as a:
            async def fn(task, msg):
                if c.count > 3:
                    return task.fail()
                log.append(c.count)

            a.use(fn)

    c.run(max_steps=200)

    assert log == [1, 2, 3]
    assert c.status is Status.FAILURE


def test_counter_runs_children_in_order(runner):
    log = []

    with counter(1, 3) as c:
        with action() as a:
            a.use(recorder(log, "first"))
        with action() as a:
            a.use(recorder(log, "second"))

    c.run(max_steps=200)

    assert log == ["first", "second", "first", "second"]


def test_empty_counter_range_succeeds(runner):
    log = []

    with counter(1, 1) as c:
        with action() as a:
            a.use(recorder(log, "never"))

    c.run(max_steps=200)

    assert log == []
    assert c.status is Status.SUCCESS


#
# LOOP
#
def test_loop_repeats_until_child_fails(runner):
    """Loop has no terminating condition of its own -- a child failure is the
    only ordinary exit."""
    log = []
    limit = 4

    with loop() as l:
        with action() as a:
            async def fn(task, msg):
                if len(log) >= limit:
                    return task.fail()
                log.append("tick")

            a.use(fn)

    l.run(max_steps=200)

    assert log == ["tick"] * limit
    assert l.status is Status.FAILURE


def test_loop_cancel_stops_it(runner):
    """The other way out: teardown."""
    log = []

    with loop() as l:
        with action() as a:
            async def fn(task, msg):
                log.append("tick")
                await task.sleep()

            a.use(fn)

    runner.schedule(l)
    step_until(runner, lambda: len(log) >= 2)

    l.cancel()
    before = len(log)
    drain(runner)

    assert len(log) == before
    assert l.status is Status.CANCELLED


def test_loop_runs_children_in_order(runner):
    log = []
    passes = 3

    with loop() as l:
        with action() as a:
            a.use(recorder(log, "first"))
        with action() as a:
            async def fn(task, msg):
                log.append("second")
                if log.count("second") >= passes:
                    return task.fail()

            a.use(fn)

    l.run(max_steps=200)

    assert log == ["first", "second"] * passes


#
# TIMER
#
def test_timer_succeeds_when_children_finish(runner):
    log = []

    with timer(1.0) as t:
        with action() as a:
            a.use(recorder(log, "quick"))

    t.run(dt=0.1, max_steps=200)

    assert log == ["quick"]
    assert t.status is Status.SUCCESS


def test_timer_fails_when_deadline_passes(runner):
    """The deadline is only checked between children, so it cannot interrupt
    one mid-run. Two children with a sleep between them is what it can catch."""
    log = []

    with timer(0.5) as t:
        with action() as a:
            a.use(recorder(log, "first", sleeps=20))
        with action() as a:
            a.use(recorder(log, "second"))

    t.run(dt=0.1, max_steps=200)

    assert log == ["first"], "second child ran past the deadline"
    assert t.status is Status.FAILURE


def test_timer_propagates_child_failure(runner):
    log = []

    with timer(1.0) as t:
        with action() as a:
            a.use(recorder(log, "first", status=Status.FAILURE))
        with action() as a:
            a.use(recorder(log, "second"))

    t.run(dt=0.1, max_steps=200)

    assert log == ["first"]
    assert t.status is Status.FAILURE


#
# FOREVER
#
def test_forever_ignores_child_failure(runner):
    """Unlike Loop, Forever restarts a failed child rather than exiting."""
    log = []

    with forever() as f:
        with action() as a:
            async def fn(task, msg):
                log.append("tick")
                return task.fail()

            a.use(fn)

    runner.schedule(f)
    step_until(runner, lambda: len(log) >= 3, max_steps=60)

    f.cancel()
    drain(runner)

    assert len(log) >= 3
    assert f.status is Status.CANCELLED


def test_forever_needs_cancel_to_stop(runner):
    log = []

    with forever() as f:
        with action() as a:
            a.use(recorder(log, "tick"))

    runner.schedule(f)
    step_until(runner, lambda: len(log) >= 3, max_steps=60)

    runner.cancel_all()

    assert runner.queue == []
    assert f.status.done


#
# NESTED REPETITION
#
# `begin()` re-arms a task's own coroutine but leaves its descendants
# finished, so a repeating composite whose child is itself a composite only
# works on the first pass. These pin that gap until Task grows a recursive
# reset().
#
@pytest.mark.xfail(reason="begin() does not reset the child's subtree", strict=False)
def test_loop_restarts_a_nested_sequence(runner):
    log = []
    passes = 3

    with loop() as l:
        with sequence():
            with action() as a:
                a.use(recorder(log, "a"))
            with action() as a:
                async def fn(task, msg):
                    log.append("b")
                    if log.count("b") >= passes:
                        return task.fail()

                a.use(fn)

    l.run(max_steps=200)

    assert log == ["a", "b"] * passes


@pytest.mark.xfail(reason="begin() does not reset the child's subtree", strict=False)
def test_loop_around_counter(runner):
    """The original test's structure: timer > loop > counter > actions."""
    log = []
    passes = 2

    with timer(5.0) as top:
        with loop():
            with counter(1, 4) as c:
                with action() as a:
                    async def fn(task, msg):
                        log.append(c.count)
                        if len(log) >= passes * 3:
                            return task.fail()

                    a.use(fn)

    top.run(dt=0.1, max_steps=400)

    assert log == [1, 2, 3] * passes