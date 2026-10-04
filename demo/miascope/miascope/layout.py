"""Tidy tree layout: Buchheim, Jünger & Leipert (2002), iterative.

Siblings keep their order, a parent is centered over its first and last child,
nodes on the same level never overlap, and identical subtrees are drawn
identically. Runs in linear time and without recursion, so deep search trees
don't hit Python's recursion limit.

Works on any tree: pass how to get a node's children and how wide it is.
Returned x values are node centers, shifted so the leftmost edge is at 0.
"""

from __future__ import annotations

from collections.abc import Callable, Hashable, Sequence
from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Point:
    x: float
    y: float


def tidy_tree(
    root: Hashable,
    children: Callable[[Hashable], Sequence[Hashable]],
    width: Callable[[Hashable], float] = lambda node: 1.0,
    gap: float = 1.0,
    level: float = 1.0,
) -> dict[Hashable, Point]:
    top = _Box(root, None, 1, 0, width(root))
    stack = [top]
    while stack:
        box = stack.pop()
        for number, child in enumerate(children(box.node), 1):
            kid = _Box(child, box, number, box.depth + 1, width(child))
            box.children.append(kid)
            stack.append(kid)

    def separation(left: _Box, right: _Box) -> float:
        return (left.width + right.width) / 2 + gap

    for box in _post_order(top):
        if not box.children:
            continue
        default_ancestor = box.children[0]
        for kid in box.children:
            _place(kid, separation)
            default_ancestor = _apportion(kid, default_ancestor, separation)
        _execute_shifts(box)
        box.midpoint = (box.children[0].prelim + box.children[-1].prelim) / 2
    _place(top, separation)

    centers: dict[Hashable, tuple[float, int, float]] = {}
    stack2 = [(top, 0.0)]
    while stack2:
        box, modsum = stack2.pop()
        centers[box.node] = (box.prelim + modsum, box.depth, box.width)
        stack2.extend((kid, modsum + box.mod) for kid in box.children)

    left_edge = min(x - w / 2 for x, _, w in centers.values())
    return {node: Point(x - left_edge, depth * level) for node, (x, depth, _) in centers.items()}


class _Box:
    __slots__ = (
        "node", "parent", "children", "number", "depth", "width",
        "prelim", "mod", "shift", "change", "midpoint", "thread", "ancestor",
    )

    def __init__(self, node, parent: _Box | None, number: int, depth: int, width: float):
        self.node = node
        self.parent = parent
        self.children: list[_Box] = []
        self.number = number
        self.depth = depth
        self.width = width
        self.prelim = self.mod = self.shift = self.change = self.midpoint = 0.0
        self.thread: _Box | None = None
        self.ancestor: _Box = self

    def next_left(self) -> _Box | None:
        return self.thread or (self.children[0] if self.children else None)

    def next_right(self) -> _Box | None:
        return self.thread or (self.children[-1] if self.children else None)

    def left_sibling(self) -> _Box | None:
        return self.parent.children[self.number - 2] if self.parent and self.number > 1 else None

    def leftmost_sibling(self) -> _Box:
        return self.parent.children[0] if self.parent else self


def _post_order(top: _Box) -> list[_Box]:
    order, stack = [], [(top, 0)]
    while stack:
        box, index = stack.pop()
        if index < len(box.children):
            stack.append((box, index + 1))
            stack.append((box.children[index], 0))
        else:
            order.append(box)
    return order


def _place(box: _Box, separation) -> None:
    # Done in the parent's loop, after the left sibling has been apportioned,
    # which matches the order of the recursive algorithm.
    sibling = box.left_sibling()
    if sibling is None:
        box.prelim = box.midpoint
    else:
        box.prelim = sibling.prelim + separation(sibling, box)
        if box.children:
            box.mod = box.prelim - box.midpoint


def _apportion(v: _Box, default_ancestor: _Box, separation) -> _Box:
    w = v.left_sibling()
    if w is None:
        return default_ancestor
    vir = vor = v
    vil = w
    vol = v.leftmost_sibling()
    sir = sor = v.mod
    sil = vil.mod
    sol = vol.mod
    while (next_vil := vil.next_right()) and (next_vir := vir.next_left()):
        vil, vir = next_vil, next_vir
        vol = vol.next_left()
        vor = vor.next_right()
        vor.ancestor = v
        shift = (vil.prelim + sil) - (vir.prelim + sir) + separation(vil, vir)
        if shift > 0:
            ancestor = vil.ancestor if vil.ancestor.parent is v.parent else default_ancestor
            _move_subtree(ancestor, v, shift)
            sir += shift
            sor += shift
        sil += vil.mod
        sir += vir.mod
        sol += vol.mod
        sor += vor.mod
    if vil.next_right() and not vor.next_right():
        vor.thread = vil.next_right()
        vor.mod += sil - sor
    else:
        if vir.next_left() and not vol.next_left():
            vol.thread = vir.next_left()
            vol.mod += sir - sol
        default_ancestor = v
    return default_ancestor


def _move_subtree(wl: _Box, wr: _Box, shift: float) -> None:
    subtrees = wr.number - wl.number
    wr.change -= shift / subtrees
    wr.shift += shift
    wl.change += shift / subtrees
    wr.prelim += shift
    wr.mod += shift


def _execute_shifts(v: _Box) -> None:
    shift = change = 0.0
    for w in reversed(v.children):
        w.prelim += shift
        w.mod += shift
        change += w.change
        shift += w.shift + change
