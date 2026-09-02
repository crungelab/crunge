import logging

import pytest
from loguru import logger


@pytest.fixture(autouse=True)
def quiet_logs():
    """Silence loguru below WARNING for the duration of each test.

    Removes the default stderr sink and installs a WARNING-level one, so
    genuine problems still surface but the per-task cancel/fail debug traffic
    stays out of the suite output. Opt back in with the `loud_logs` fixture.
    """
    logger.remove()
    handler_id = logger.add(
        lambda msg: print(msg, end=""),
        level="WARNING",
        format="{level: <8} | {name}:{function}:{line} - {message}",
    )
    yield
    logger.remove(handler_id)


@pytest.fixture
def loud_logs():
    """Restore DEBUG-level output for a single test.

    Request alongside the autouse fixture; this one runs later and wins.

        def test_something(runner, loud_logs):
            ...
    """
    logger.remove()
    handler_id = logger.add(
        lambda msg: print(msg, end=""),
        level="DEBUG",
        format="{level: <8} | {name}:{function}:{line} - {message}",
    )
    yield
    logger.remove(handler_id)


@pytest.fixture
def logs():
    """Capture loguru records so a test can assert on them.

        def test_runaway(runner, logs):
            ...
            assert logs.contains("exceeded", level="ERROR")
    """

    class Capture:
        def __init__(self):
            self.records = []

        def __call__(self, message):
            record = message.record
            self.records.append((record["level"].name, record["message"]))

        def contains(self, text, level=None):
            return any(
                text in msg and (level is None or lvl == level)
                for lvl, msg in self.records
            )

        @property
        def messages(self):
            return [msg for _, msg in self.records]

    capture = Capture()
    logger.remove()
    handler_id = logger.add(capture, level="DEBUG")
    yield capture
    logger.remove(handler_id)


@pytest.fixture(autouse=True)
def clean_task_ctx():
    """Reset the DSL's context vars between tests.

    task_ctx_parent is module-global. A test that fails inside a `with` block
    leaves it dangling, and the next test's tree attaches to the wrong parent.
    """
    from crunge.engine.ai.bt.run.act.helpers import (
        agent_ctx_root,
        task_ctx_parent,
        neuron_ctx_root,
        neuron_ctx_parent,
    )

    agent_ctx_root.set(None)
    task_ctx_parent.set(None)
    neuron_ctx_root.set(None)
    neuron_ctx_parent.set(None)
    yield
    agent_ctx_root.set(None)
    task_ctx_parent.set(None)
    neuron_ctx_root.set(None)
    neuron_ctx_parent.set(None)