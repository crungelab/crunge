"""What the inspector shows for a node at an event index."""

from __future__ import annotations

from dataclasses import dataclass, field

from .model import Node, Trace


@dataclass(frozen=True, slots=True)
class ContextRow:
    clause: str
    change: str  # "added" or "kept" (in the context), or "removed" (gone relative to the parent)

    def matches(self, text: str) -> bool:
        return not text or text.lower() in self.clause.lower()


@dataclass
class Report:
    fields: list[tuple[str, str]]
    proposals: list[dict] = field(default_factory=list)
    suspended: list[dict] = field(default_factory=list)
    context: list[ContextRow] = field(default_factory=list)


def report(trace: Trace, node: Node, t: int | None = None) -> Report:
    phase = node.phase(t)
    state = node.state if node.reached is not None and (t is None or node.reached <= t) else None
    fields = [
        ("agent", str(node.id)),
        ("search", node.search.agent if node.search else "?"),
        ("phase", phase.value if phase else "not created yet"),
        ("proposal", node.proposal or "-"),
    ]
    if node.plan:
        fields.append(("plan", node.plan))
    if state is None:
        return Report(fields)
    fields += [
        ("depth", str(state["depth"])),
        ("cost", f"{state['cost']:g}"),
        ("priority", f"{state['priority']:g}"),
    ]
    added = set(state["added"]) if node.parent is not None else set()
    rows = [ContextRow(c, "added" if c in added else "kept") for c in trace.context(node)]
    if node.parent is not None:
        rows += [ContextRow(c, "removed") for c in state["removed"]]
    return Report(fields, state["proposals"], state["suspended"], rows)
