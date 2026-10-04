"""miascope's model of a trace: states, problem spaces, and replay over time.

Built only from trace events, so miascope never imports the Mia runtime or the
program that produced the trace.

Time is an event index. A node exists from the event that created it (fork,
spawn, or space), is queued once its `status` event arrives, and is resolved by
its outcome event (expand, prune, skip, dead, or solution). `Node.phase(t)`
answers "what was this state doing at event t" for a timeline slider.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

from crunge.mia.runtime.trace import TRACE_VERSION


class TraceError(ValueError):
    pass


class Phase(Enum):
    RUNNING = "running"    # created, still advancing to its next decision
    QUEUED = "queued"      # reached a decision or finished; waiting in the frontier
    EXPANDED = "expanded"  # its proposals were forked
    PRUNED = "pruned"      # its state was already reached at lower or equal cost
    SKIPPED = "skipped"    # a cheaper path to its state was found while it waited
    DEAD = "dead"          # finished without success
    SOLUTION = "solution"


_OUTCOMES = {
    "expand": Phase.EXPANDED,
    "prune": Phase.PRUNED,
    "skip": Phase.SKIPPED,
    "dead": Phase.DEAD,
    "solution": Phase.SOLUTION,
}


@dataclass(eq=False)
class Node:
    """One state: a node in its search tree."""

    id: int
    created: int
    space: Space | None = None
    parent: Node | None = None  # the state it was forked from; None for a space root
    children: list[Node] = field(default_factory=list)
    spawned: list[Space] = field(default_factory=list)
    proposal: str | None = None  # the proposal it committed to, or the message that spawned it
    plan: str | None = None  # the plan chosen, when several matched
    state: dict | None = None
    actions: list[str] = field(default_factory=list)  # `||` lines this state recorded
    reached: int | None = None
    resolved: int | None = None
    outcome: Phase | None = None

    @property
    def label(self) -> str:
        if self.parent is None and self.space is not None:
            return self.space.label
        text = self.proposal or f"state {self.id}"
        return f"{text} [{self.plan}]" if self.plan else text

    @property
    def cost(self) -> float | None:
        return self.state["cost"] if self.state else None

    @property
    def priority(self) -> float | None:
        return self.state["priority"] if self.state else None

    def phase(self, t: int | None = None) -> Phase | None:
        """What this state was doing at event `t` (the end of the trace if None)."""
        if t is not None and self.created > t:
            return None
        if self.resolved is not None and (t is None or self.resolved <= t):
            return self.outcome
        if self.reached is not None and (t is None or self.reached <= t):
            return Phase.QUEUED
        return Phase.RUNNING

    def display_children(self) -> list[Node]:
        """Forks, then the roots of experts this state spawned."""
        return self.children + [space.root for space in self.spawned]


@dataclass(eq=False)
class Space:
    """One problem space: a search tree rooted at a state."""

    id: int
    root: Node
    experts: tuple[str, ...]   # the experts active in this space's root state
    priority: str
    spawner: Node | None
    nodes: list[Node] = field(default_factory=list)
    solution: Node | None = None
    expansions: int = 0
    exhausted: bool = False
    finished: int | None = None

    @property
    def expert(self) -> str:
        """The active experts as one name, for headings."""
        return " + ".join(self.experts)

    @property
    def label(self) -> str:
        return " + ".join(e.rsplit(".", 1)[-1] for e in self.experts)


class Trace:
    def __init__(self, events: list[dict]):
        self.events = events
        self.header: dict = {}
        self.nodes: dict[int, Node] = {}
        self.spaces: dict[int, Space] = {}
        for index, event in enumerate(events):
            self._apply(index, event)
        tops = [s for s in self.spaces.values() if s.spawner is None]
        if len(tops) != 1:
            raise TraceError(f"expected one top-level problem space, found {len(tops)}")
        self.top: Space = tops[0]

    @classmethod
    def load(cls, path: str | Path) -> Trace:
        with open(path, encoding="utf-8") as f:
            return cls.loads(f.read())

    @classmethod
    def loads(cls, text: str) -> Trace:
        """A trace from JSON-lines text."""
        return cls([json.loads(line) for line in text.splitlines() if line.strip()])

    # ------------------------------------------------------------ queries

    def path(self, node: Node) -> list[Node]:
        """From the node's space root down to the node."""
        path = [node]
        while path[-1].parent is not None:
            path.append(path[-1].parent)
        return path[::-1]

    def context(self, node: Node) -> list[str]:
        """The node's whole context, rebuilt from the changes recorded along its path."""
        clauses: dict[str, None] = {}
        for step in self.path(node):
            if step.state is None:
                raise TraceError(f"state {step.id} has no recorded status")
            for clause in step.state["removed"]:
                clauses.pop(clause, None)
            for clause in step.state["added"]:
                clauses.pop(clause, None)  # re-adding moves a clause to the end, as in a Context
                clauses[clause] = None
        return list(clauses)

    def solution_path(self, space: Space) -> list[Node]:
        return self.path(space.solution) if space.solution is not None else []

    def plan(self, node: Node) -> list[str]:
        """The actions along the path to `node`, including those of experts it
        spawned along the way — the same order the runtime would replay them."""
        actions: list[str] = []
        for step in self.path(node):
            actions += step.actions
            for space in step.spawned:
                if space.solution is not None:
                    actions += self.plan(space.solution)
        return actions

    # ------------------------------------------------------------ building

    def _apply(self, index: int, event: dict):
        kind = event.get("event")
        match kind:
            case "trace":
                if event.get("version") != TRACE_VERSION:
                    raise TraceError(
                        f"trace version {event.get('version')} is not supported; "
                        f"miascope reads version {TRACE_VERSION}"
                    )
                self.header = event
            case "spawn":
                node = self._node(event["state"], index)
                node.proposal = event["message"]
            case "space":
                root = self._node(event["root"], index)
                spawner = self._existing(event["parent"]) if event["parent"] is not None else None
                experts = tuple(event["expert"].split(" + "))
                space = Space(event["space"], root, experts, event["priority"], spawner, [root])
                self.spaces[space.id] = space
                root.space = space
                if spawner is not None:
                    spawner.spawned.append(space)
            case "fork":
                parent = self._existing(event["parent"])
                node = self._node(event["state"], index)
                node.parent, node.space = parent, parent.space
                node.proposal, node.plan = event["proposal"], event.get("plan")
                parent.children.append(node)
                if parent.space is not None:
                    parent.space.nodes.append(node)
            case "status":
                node = self._existing(event["state"])
                node.state, node.reached = event, index
            case "action":
                self._existing(event["state"]).actions.append(event["text"])
            case _ if kind in _OUTCOMES:
                node = self._existing(event["state"])
                node.outcome, node.resolved = _OUTCOMES[kind], index
                if kind == "solution":
                    self._space(event).solution = node
            case "exhausted":
                self._space(event).exhausted = True
            case "result":
                space = self._space(event)
                space.expansions, space.finished = event["expansions"], index
            case _:
                pass  # unknown events are ignored, so newer traces still load

    def _node(self, state_id: int, index: int) -> Node:
        node = self.nodes.get(state_id)
        if node is None:
            node = self.nodes[state_id] = Node(state_id, index)
        return node

    def _existing(self, state_id: int) -> Node:
        try:
            return self.nodes[state_id]
        except KeyError:
            raise TraceError(f"event refers to state {state_id} before it was created") from None

    def _space(self, event: dict) -> Space:
        try:
            return self.spaces[event["space"]]
        except KeyError:
            raise TraceError(f"event refers to unknown problem space {event.get('space')}") from None
