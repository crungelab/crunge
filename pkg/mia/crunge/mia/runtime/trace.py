"""Tracing: record what experts and problem spaces do, for miascope.

A trace is a sequence of events. Each event is a JSON-compatible dict with an
"event" field, and runtime values are rendered in Mia syntax when recorded, so
a trace can be read without importing the runtime or the program.

Events, in the order they can occur:

  trace     header: version, expert class, start time
  space     a search begins: space, root state, parent state, expert, priority
  fork      a child state is created: state, parent, proposal
  spawn     an expert starts in a child space: state, parent, expert, message
  status    a state reached a decision or finished: cost, priority, context
            changes against its parent (the whole context for a root),
            proposals, suspended tasks
  action    a `||` line this state recorded for its plan: text
  prune     this state was already reached at lower or equal cost: best
  expand    the space forks this state's proposals
  skip      popped, but a cheaper path to the same state was found since
  dead      popped, finished without success
  solution  popped, finished successfully
  exhausted the expansion limit was reached
  result    the search ended: solution (or null), expansions

Tracing costs almost nothing when off: the runtime checks `tracer is not None`
before building any event.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from itertools import count
from pathlib import Path

from .format import to_mia

TRACE_VERSION = 2


class ListSink:
    def __init__(self):
        self.events: list[dict] = []

    def write(self, event: dict):
        self.events.append(event)

    def close(self):
        pass


class JsonlSink:
    def __init__(self, path: str | Path):
        self._file = open(path, "w", encoding="utf-8")

    def write(self, event: dict):
        self._file.write(json.dumps(event) + "\n")

    def close(self):
        self._file.close()


class Tracer:
    def __init__(self, sink):
        self.sink = sink
        self._ids = count(1)

    def next_id(self) -> int:
        return next(self._ids)

    def emit(self, event: str, **fields):
        self.sink.write({"event": event, **fields})

    def header(self, expert_class: type):
        self.emit(
            "trace",
            version=TRACE_VERSION,
            expert=expert_class.__qualname__,
            started=datetime.now(timezone.utc).isoformat(timespec="seconds"),
        )

    def close(self):
        self.sink.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()


def read_trace(path: str | Path) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


# ---------------------------------------------------------------- snapshots


def context_changes(state, base) -> dict:
    """Clauses added and removed relative to `base` (all of them if `base` is None)."""
    now = state.context
    if base is None:
        return {"added": [to_mia(c) for c in now], "removed": []}
    before = base.context
    return {
        "added": [to_mia(c) for c in now if c not in before],
        "removed": [to_mia(c) for c in before if c not in now],
    }


def proposals(state) -> list[dict]:
    from .expert import _plan_name

    return [{"message": to_mia(p.message), "plan": _plan_name(p.plan)} for p in state.proposals]


def suspended(state) -> list[dict]:
    return [
        {
            "task": type(task).__qualname__,
            "pc": task.pc,
            "vars": {k[2:]: to_mia(v) for k, v in vars(task).items() if k.startswith("v_")},
        }
        for task in state.suspended
    ]
