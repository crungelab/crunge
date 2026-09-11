"""miascope's model of a trace: agents, searches, and replay over time.

Built only from trace events, so miascope never imports the Mia runtime or the
program that produced the trace.

Time is an event index. A node exists from the event that created it (fork,
spawn, or agency), is queued once its `state` event arrives, and is resolved by
its outcome event (expand, prune, skip, dead, or solution). `Node.phase(t)`
answers "what was this agent doing at event t" for a timeline slider.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path


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
    """One agent: a node in its search tree."""

    id: int
    created: int
    search: Search | None = None
    parent: Node | None = None  # the agent it was forked from; None for a search root
    children: list[Node] = field(default_factory=list)
    spawned: list[Search] = field(default_factory=list)
    proposal: str | None = None  # the proposal it committed to, or the message that spawned it
    plan: str | None = None  # the plan chosen, when several matched
    state: dict | None = None
    reached: int | None = None
    resolved: int | None = None
    outcome: Phase | None = None

    @property
    def label(self) -> str:
        if self.parent is None and self.search is not None:
            return self.search.agent.rsplit(".", 1)[-1]
        text = self.proposal or f"agent {self.id}"
        return f"{text} [{self.plan}]" if self.plan else text

    @property
    def cost(self) -> float | None:
        return self.state["cost"] if self.state else None

    @property
    def priority(self) -> float | None:
        return self.state["priority"] if self.state else None

    def phase(self, t: int | None = None) -> Phase | None:
        """What this agent was doing at event `t` (the end of the trace if None)."""
        if t is not None and self.created > t:
            return None
        if self.resolved is not None and (t is None or self.resolved <= t):
            return self.outcome
        if self.reached is not None and (t is None or self.reached <= t):
            return Phase.QUEUED
        return Phase.RUNNING

    def display_children(self) -> list[Node]:
        """Forks, then the roots of experts this agent spawned."""
        return self.children + [search.root for search in self.spawned]


@dataclass(eq=False)
class Search:
    """One agency: a search tree rooted at an agent."""

    id: int
    root: Node
    agent: str
    priority: str
    spawner: Node | None
    nodes: list[Node] = field(default_factory=list)
    solution: Node | None = None
    expansions: int = 0
    exhausted: bool = False
    finished: int | None = None


class Trace:
    def __init__(self, events: list[dict]):
        self.events = events
        self.header: dict = {}
        self.nodes: dict[int, Node] = {}
        self.searches: dict[int, Search] = {}
        for index, event in enumerate(events):
            self._apply(index, event)
        tops = [s for s in self.searches.values() if s.spawner is None]
        if len(tops) != 1:
            raise TraceError(f"expected one top-level search, found {len(tops)}")
        self.top: Search = tops[0]

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
        """From the node's search root down to the node."""
        path = [node]
        while path[-1].parent is not None:
            path.append(path[-1].parent)
        return path[::-1]

    def context(self, node: Node) -> list[str]:
        """The node's whole context, rebuilt from the changes recorded along its path."""
        clauses: dict[str, None] = {}
        for step in self.path(node):
            if step.state is None:
                raise TraceError(f"agent {step.id} has no recorded state")
            for clause in step.state["removed"]:
                clauses.pop(clause, None)
            for clause in step.state["added"]:
                clauses.pop(clause, None)  # re-adding moves a clause to the end, as in a Context
                clauses[clause] = None
        return list(clauses)

    def solution_path(self, search: Search) -> list[Node]:
        return self.path(search.solution) if search.solution is not None else []

    # ------------------------------------------------------------ building

    def _apply(self, index: int, event: dict):
        kind = event.get("event")
        match kind:
            case "trace":
                self.header = event
            case "spawn":
                node = self._node(event["agent"], index)
                node.proposal = event["message"]
            case "agency":
                root = self._node(event["root"], index)
                spawner = self._existing(event["parent"]) if event["parent"] is not None else None
                search = Search(event["agency"], root, event["agent"], event["priority"], spawner, [root])
                self.searches[search.id] = search
                root.search = search
                if spawner is not None:
                    spawner.spawned.append(search)
            case "fork":
                parent = self._existing(event["parent"])
                node = self._node(event["agent"], index)
                node.parent, node.search = parent, parent.search
                node.proposal, node.plan = event["proposal"], event.get("plan")
                parent.children.append(node)
                if parent.search is not None:
                    parent.search.nodes.append(node)
            case "state":
                node = self._existing(event["agent"])
                node.state, node.reached = event, index
            case _ if kind in _OUTCOMES:
                node = self._existing(event["agent"])
                node.outcome, node.resolved = _OUTCOMES[kind], index
                if kind == "solution":
                    self._search(event).solution = node
            case "exhausted":
                self._search(event).exhausted = True
            case "result":
                search = self._search(event)
                search.expansions, search.finished = event["expansions"], index
            case _:
                pass  # unknown events are ignored, so newer traces still load

    def _node(self, agent_id: int, index: int) -> Node:
        node = self.nodes.get(agent_id)
        if node is None:
            node = self.nodes[agent_id] = Node(agent_id, index)
        return node

    def _existing(self, agent_id: int) -> Node:
        try:
            return self.nodes[agent_id]
        except KeyError:
            raise TraceError(f"event refers to agent {agent_id} before it was created") from None

    def _search(self, event: dict) -> Search:
        try:
            return self.searches[event["agency"]]
        except KeyError:
            raise TraceError(f"event refers to unknown agency {event.get('agency')}") from None
