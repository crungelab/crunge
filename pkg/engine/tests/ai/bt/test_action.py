import gc
import weakref

import pytest

from crunge.engine.ai.bt.run.act import *
from crunge.engine.ai.bt.run.task import Task, Runner, Sleep, NoOp, Status


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
    """Step until the queue empties. Fails loudly rather than hanging."""
    steps = 0
    while runner.queue:
        assert steps < max_steps, f"queue did not drain in {max_steps} steps"
        runner.step(dt)
        steps += 1
    return steps


#
# COMPLETION SEMANTICS
#
def test_bare_return_is_success(runner):
    """`main` returning None still means success -- the ergonomics that
    TS_SUCCESS = None used to provide, now handled at the status layer."""
    calls = []

    async def fn(task, msg):
        calls.append(msg)

    task = Task(fn, "hello")
    runner.schedule(task)
    drain(runner)

    assert calls == ["hello"]
    assert task.status is Status.SUCCESS
    assert task.result is None


def test_explicit_fail(runner):
    async def fn(task, msg):
        return task.fail()

    task = Task(fn)
    runner.schedule(task)
    drain(runner)

    assert task.status is Status.FAILURE


def test_returned_status_is_honored(runner):
    """`return Status.FAILURE` without calling fail()."""
    async def fn(task, msg):
        return Status.FAILURE

    task = Task(fn)
    runner.schedule(task)
    drain(runner)

    assert task.status is Status.FAILURE


def test_payload_return_does_not_read_as_status(runner):
    """The result channel is free now that success is not None."""
    async def fn(task, msg):
        return 42

    task = Task(fn)
    runner.schedule(task)
    drain(runner)

    assert task.status is Status.SUCCESS
    assert task.result == 42


def test_direct_status_assignment(runner):
    """Bot.main ends with `self.status = X; return self.status`."""
    async def fn(task, msg):
        task.status = Status.SUCCESS
        return task.status

    task = Task(fn)
    runner.schedule(task)
    drain(runner)

    assert task.status is Status.SUCCESS


#
# AWAIT
#
def test_await_delivers_child_result(runner):
    async def child_fn(task, msg):
        return "payload"

    child = Task(child_fn)
    seen = []

    async def parent_fn(task, msg):
        seen.append(await child)

    parent = Task(parent_fn)
    runner.schedule(parent)
    drain(runner)

    assert seen == ["payload"]
    assert parent.status is Status.SUCCESS
    assert child.status is Status.SUCCESS


def test_last_awaited_exposes_child_status(runner):
    """How a composite branches now that the await value is a payload."""
    async def child_fn(task, msg):
        return task.fail()

    child = Task(child_fn)
    observed = []

    async def parent_fn(task, msg):
        await child
        observed.append(task.last_awaited.status)

    parent = Task(parent_fn)
    runner.schedule(parent)
    drain(runner)

    assert observed == [Status.FAILURE]


def test_bare_sleep_yields_control(runner):
    """`await self.sleep()` with no period reschedules for the next step."""
    ticks = []

    async def fn(task, msg):
        for i in range(3):
            ticks.append(i)
            await task.sleep()

    task = Task(fn)
    runner.schedule(task)

    runner.step()
    assert ticks == [0]
    runner.step()
    assert ticks == [0, 1]

    drain(runner)
    assert ticks == [0, 1, 2]
    assert task.status is Status.SUCCESS


#
# FAILURE CONTAINMENT
#
def test_exception_fails_only_the_raising_task(runner):
    """Previously an exception escaped step() and silently dropped every
    remaining task in the batch."""
    ran = []

    async def boom(task, msg):
        raise ValueError("boom")

    async def survivor(task, msg):
        ran.append("survivor")

    bad = Task(boom)
    good = Task(survivor)
    runner.schedule(bad)
    runner.schedule(good)

    assert len(runner.queue) == 2
    runner.step()

    assert bad.status is Status.FAILURE
    assert isinstance(bad.error, ValueError)
    assert ran == ["survivor"]
    assert good.status is Status.SUCCESS


def test_exception_wakes_the_awaiter(runner):
    async def boom(task, msg):
        raise ValueError("boom")

    child = Task(boom)
    resumed = []

    async def parent_fn(task, msg):
        await child
        resumed.append(task.last_awaited.status)

    parent = Task(parent_fn)
    runner.schedule(parent)
    drain(runner)

    assert resumed == [Status.FAILURE]
    assert parent.status is Status.SUCCESS


#
# CANCELLATION
#
def test_cancel_stops_execution(runner):
    """Cancellation used to be advisory -- status was set but the task kept
    getting sent to."""
    ticks = []

    async def fn(task, msg):
        while True:
            ticks.append(1)
            await task.sleep()

    task = Task(fn)
    runner.schedule(task)

    runner.step()
    assert len(ticks) == 1

    task.cancel()
    runner.step()
    runner.step()

    assert len(ticks) == 1
    assert task.status is Status.CANCELLED
    assert task.coro is None


def test_cancel_recurses_to_children(runner):
    parent = Task()
    child = Task()
    grandchild = Task()
    parent.add(child)
    child.add(grandchild)

    parent.cancel()

    assert child.status is Status.CANCELLED
    assert grandchild.status is Status.CANCELLED


def test_cancel_wakes_the_awaiter(runner):
    """A composite blocked on a cancelled child must not hang."""
    async def forever_fn(task, msg):
        while True:
            await task.sleep()

    child = Task(forever_fn)
    observed = []

    async def parent_fn(task, msg):
        await child
        observed.append(task.last_awaited.status)

    parent = Task(parent_fn)
    runner.schedule(parent)
    runner.step()

    assert parent.status is Status.SUSPENDED

    child.cancel()
    drain(runner)

    assert observed == [Status.CANCELLED]


def test_finally_runs_on_cancel(runner):
    """What the actions rely on for state cleanup."""
    cleaned = []

    async def fn(task, msg):
        try:
            while True:
                await task.sleep()
        finally:
            cleaned.append(task.status)

    task = Task(fn)
    runner.schedule(task)
    runner.step()

    task.cancel()
    assert cleaned == [Status.CANCELLED]


def test_cancel_all_releases_references(runner):
    """The leak behind resetting the scene: a suspended frame holds the task,
    which holds the agent, which holds the node."""
    class Node:
        pass

    node = Node()
    ref = weakref.ref(node)

    async def fn(task, msg):
        held = node  # noqa: F841 -- captured in the frame on purpose
        while True:
            await task.sleep()

    task = Task(fn)
    runner.schedule(task)
    runner.step()

    del node
    gc.collect()
    assert ref() is not None, "frame should still hold it while suspended"

    runner.cancel_all()
    del task
    gc.collect()

    assert ref() is None
    assert runner.queue == []


def test_reschedule_refuses_finished_task(runner):
    task = Task()
    task.cancel()
    runner.reschedule(task)
    assert runner.queue == []


#
# SLEEP AND RUNNER TIME
#
def test_sleep_uses_runner_time(runner):
    """Sleep is on the runner clock, not wall clock, so pause and slow motion
    work without special handling."""
    done = []

    async def fn(task, msg):
        elapsed = await task.sleep(1.0)
        done.append(elapsed)

    task = Task(fn)
    runner.schedule(task)

    for _ in range(4):
        runner.step(0.25)
    assert done == []

    for _ in range(2):
        runner.step(0.25)

    assert len(done) == 1
    assert done[0] >= 1.0
    assert task.status is Status.SUCCESS


def test_sleep_does_not_advance_without_dt(runner):
    """A paused game freezes the trees."""
    done = []

    async def fn(task, msg):
        await task.sleep(1.0)
        done.append(True)

    runner.schedule(Task(fn))

    for _ in range(20):
        runner.step(0.0)

    assert done == []


def test_sleep_start_captured_at_begin(runner):
    """Not at construction -- otherwise any delay in between is eaten from
    the period."""
    sleep = Sleep(1.0)
    runner.time = 10.0
    runner._admit(sleep)

    assert sleep.start == 10.0


def test_run_drives_to_completion(runner):
    async def fn(task, msg):
        await task.sleep(0.5)
        return "done"

    task = Task(fn)
    result = task.run(dt=0.1)

    assert result == "done"
    assert task.status is Status.SUCCESS


def test_run_aborts_on_runaway(runner):
    """dt=0 against a Sleep would otherwise spin forever."""
    async def fn(task, msg):
        await task.sleep(1.0)

    task = Task(fn)
    task.run(dt=0.0, max_steps=10)

    assert runner.queue == []


#
# TRAPS AND VALIDATION
#
def test_noop_succeeds(runner):
    task = NoOp()
    runner.schedule(task)
    drain(runner)
    assert task.status is Status.SUCCESS


def test_schedule_rejects_non_task(runner):
    with pytest.raises(TypeError):
        runner.schedule(object())


def test_use_rejects_plain_function(runner):
    def not_a_coro(task, msg):
        pass

    with pytest.raises(TypeError):
        Task().use(not_a_coro)


#
# DSL
#
def test_action_dsl(runner):
    """The original test, with assertions."""
    calls = []

    with action() as a:  # ASSUMPTION: action() yields the Action itself
        async def fn(task, msg):
            calls.append("ran")

        a.use(fn)
        a.run()

    assert calls == ["ran"]
    assert a.status is Status.SUCCESS

def test_cancel_all_converges_with_awaiters(runner):
    """Cancelling a child wakes its awaiter, which must not survive teardown."""
    async def child_fn(task, msg):
        while True:
            await task.sleep()

    child = Task(child_fn)

    async def parent_fn(task, msg):
        await child

    parent = Task(parent_fn)
    runner.schedule(parent)
    runner.step()

    runner.cancel_all()

    assert runner.queue == []
    assert parent.status.done
    assert child.status.done


def test_cancel_all_is_idempotent(runner):
    async def fn(task, msg):
        while True:
            await task.sleep()

    runner.schedule(Task(fn))
    runner.step()

    runner.cancel_all()
    runner.cancel_all()

    assert runner.queue == []