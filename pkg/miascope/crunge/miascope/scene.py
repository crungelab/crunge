"""What to draw for a trace: node boxes and edges in world coordinates.

Independent of any drawing API. The painter asks what's visible at an event
index and in a world rectangle, and the page asks what's under the mouse.
"""

from __future__ import annotations

from collections.abc import Callable, Iterator
from dataclasses import dataclass

from .layout import tidy_tree
from .model import Node, Phase, Trace
from .style import FONT_SIZE, GAP, LEVEL, PADDING

Rect = tuple[float, float, float, float]  # left, top, right, bottom


@dataclass(frozen=True, slots=True)
class Box:
    node: Node
    left: float
    top: float
    right: float
    bottom: float

    def contains(self, x: float, y: float) -> bool:
        return self.left <= x <= self.right and self.top <= y <= self.bottom

    def overlaps(self, rect: Rect) -> bool:
        left, top, right, bottom = rect
        return self.left <= right and self.right >= left and self.top <= bottom and self.bottom >= top


@dataclass(frozen=True, slots=True)
class Edge:
    parent: Node
    child: Node
    x0: float
    y0: float
    x1: float
    y1: float
    spawn: bool      # into the root of a spawned expert's search
    solution: bool   # on a solution path

    def overlaps(self, rect: Rect) -> bool:
        left, top, right, bottom = rect
        return (min(self.x0, self.x1) <= right and max(self.x0, self.x1) >= left
                and min(self.y0, self.y1) <= bottom and max(self.y0, self.y1) >= top)


class Scene:
    def __init__(
        self,
        trace: Trace,
        measure: Callable[[str], float],
        font_size: float = FONT_SIZE,
        padding: float = PADDING,
        gap: float = GAP,
        level: float = LEVEL,
    ):
        self.trace = trace
        self.font_size = font_size
        self.padding = padding
        height = font_size + 2 * padding

        widths: dict[Node, float] = {}

        def width(node: Node) -> float:
            if node not in widths:
                widths[node] = measure(node.label) + 2 * padding
            return widths[node]

        centers = tidy_tree(trace.top.root, Node.display_children, width, gap, level)
        self.boxes: dict[Node, Box] = {
            node: Box(node, p.x - width(node) / 2, p.y, p.x + width(node) / 2, p.y + height)
            for node, p in centers.items()
        }
        self.solution: set[Node] = self._solution_nodes()
        self.edges: list[Edge] = []
        for parent, box in self.boxes.items():
            for child in parent.display_children():
                kid = self.boxes[child]
                self.edges.append(Edge(
                    parent, child,
                    (box.left + box.right) / 2, box.bottom,
                    (kid.left + kid.right) / 2, kid.top,
                    spawn=child.parent is None,
                    solution=parent in self.solution and child in self.solution,
                ))
        self.bounds: Rect = (
            min(b.left for b in self.boxes.values()),
            min(b.top for b in self.boxes.values()),
            max(b.right for b in self.boxes.values()),
            max(b.bottom for b in self.boxes.values()),
        )

    def _solution_nodes(self) -> set[Node]:
        """Solution paths, following spawned searches only from agents already on a path."""
        nodes: set[Node] = set()
        pending = [self.trace.top]
        while pending:
            search = pending.pop()
            for node in self.trace.solution_path(search):
                if node not in nodes:
                    nodes.add(node)
                    pending.extend(s for s in node.spawned if s.solution is not None)
        return nodes

    def visible(self, t: int | None = None, rect: Rect | None = None) -> Iterator[tuple[Box, Phase]]:
        for box in self.boxes.values():
            phase = box.node.phase(t)
            if phase is not None and (rect is None or box.overlaps(rect)):
                yield box, phase

    def visible_edges(self, t: int | None = None, rect: Rect | None = None) -> Iterator[Edge]:
        for edge in self.edges:
            if edge.child.phase(t) is not None and (rect is None or edge.overlaps(rect)):
                yield edge

    def hit(self, x: float, y: float, t: int | None = None) -> Node | None:
        for box in self.boxes.values():
            if box.contains(x, y) and box.node.phase(t) is not None:
                return box.node
        return None
