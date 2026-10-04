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
    experts: list[str] = field(default_factory=list)
    proposals: list[dict] = field(default_factory=list)
    suspended: list[dict] = field(default_factory=list)
    context: list[ContextRow] = field(default_factory=list)


def report(trace: Trace, node: Node, t: int | None = None) -> Report:
    phase = node.phase(t)
    state = node.state if node.reached is not None and (t is None or node.reached <= t) else None
    experts = state["experts"] if state and "experts" in state else (
        list(node.space.experts) if node.space else []
    )
    fields = [
        ("state", str(node.id)),
        ("experts", ", ".join(e.rsplit(".", 1)[-1] for e in experts) or "?"),
        ("phase", phase.value if phase else "not created yet"),
        ("proposal", node.proposal or "-"),
    ]
    if node.plan:
        fields.append(("plan", node.plan))
    short = [e.rsplit(".", 1)[-1] for e in experts]
    if state is None:
        return Report(fields, short)
    fields += [
        ("depth", str(state["depth"])),
        ("cost", f"{state['cost']:g}"),
        ("priority", f"{state['priority']:g}"),
    ]
    added = set(state["added"]) if node.parent is not None else set()
    rows = [ContextRow(c, "added" if c in added else "kept") for c in trace.context(node)]
    if node.parent is not None:
        rows += [ContextRow(c, "removed") for c in state["removed"]]
    return Report(fields, short, state["proposals"], state["suspended"], rows)
