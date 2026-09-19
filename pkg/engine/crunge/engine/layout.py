from __future__ import annotations

import math

from loguru import logger
import glm

from crunge import yoga

from crunge.core.base_node import BaseNode
from crunge.core.chip import Chip


class Layout[N: BaseNode](Chip[N]):
    """Owns a yoga layout node on behalf of the node it is seated on.

    Layout chips form their own tree, parallel to but not identical with
    the node tree: a chip links to the nearest *ancestor* node carrying a
    Layout chip, so nodes without one are skipped. Calculation is driven
    from the root; each chip whose computed layout changed calls
    `node.on_layout(self)` and lets the node decide how to read the result
    — y-down for widgets, y-up for Node2D, y onto z for Node3D.

    Dirt is yoga's, not ours. `layout_node` tracks its own dirty bit and
    propagates it to the root, and `has_new_layout()` reports per-node
    staleness after a calculation. A `Dirt` member here would be the
    duplicate source of truth the base class warns about, so this chip
    neither marks nor flushes.

    Specialize by subclassing: `Layout2D(Layout[Node2D])`.
    """

    def __init__(self, style: yoga.Style = None) -> None:
        super().__init__()
        # ASSUMPTION: cxbind rename of yoga.Layout -> yoga.LayoutNode.
        # Still `yoga.Layout` until that lands.
        self.layout_node = yoga.LayoutNode()
        self.layout_node.set_style(style or yoga.Style())

        # Layout tree, independent of the node tree.
        self.parent: Layout | None = None
        self.children: list[Layout] = []

    # -- attach lifecycle --------------------------------------------------

    '''
    def plug(self) -> None:
        """Link into the ancestor's layout node.

        Creation runs top-down, so by the time this fires the ancestor's
        Layout chip exists and has already plugged.
        """
        parent = self.find_parent()
        if parent is not None:
            parent.adopt(self)

    def unplug(self) -> None:
        exit()
        logger.debug(f"Layout.unplug: {self.node} parent={self.parent}")
        if self.parent is not None:
            self.parent.abandon(self)
    '''

    def plug(self) -> None:
        """Link a node that was already in the tree when its chips were created."""
        if self.parent is None:
            self.on_added()

    def on_added(self) -> None:
        """Link a node inserted into a tree that already exists."""
        if self.parent is not None:
            return
        parent = self.find_parent()
        if parent is not None:
            parent.adopt(self)

    def unplug(self) -> None:
        """Unlink a node whose chips are being torn down while it is still
        in the tree. Runs while the chip set is intact, so siblings and
        the parent chain are safe to touch."""
        self.on_removed()

    def on_removed(self) -> None:
        """Unlink a node being taken out of the tree."""
        if self.parent is None:
            return
        self.parent.abandon(self)

    # -- layout tree -------------------------------------------------------

    def find_parent(self) -> Layout | None:
        """Nearest ancestor node carrying a Layout chip, or None."""
        node = self.node.parent
        while node is not None:
            # ASSUMPTION: a non-raising counterpart to `require` that
            # matches subclasses. `require` is wrong here — an ancestor
            # without layout is the normal case, not an error.
            layout = node.get_chip(Layout)
            if layout is not None:
                return layout
            node = node.parent
        return None

    def adopt(self, child: Layout) -> None:
        index = self.index_of(child)
        child.parent = self
        self.children.insert(index, child)
        self.layout_node.insert_child(child.layout_node, index)  # ASSUMPTION

    def index_of(self, child: Layout) -> int:
        """Where `child` belongs among our layout children, by node order."""
        index = 0
        for node in self.node.children:
            if node is child.node:
                return index
            layout = node.get_chip(Layout)
            if layout is not None and layout.parent is self:
                index += 1
        return index

    '''
    def adopt(self, child: Layout) -> None:
        # NOTE: append only. Flex order follows plug order, which matches
        # node order for a tree built top-down. Re-parenting a subtree into
        # the middle of another would need insert_child(index); the old
        # Widget code had the same limitation.
        child.parent = self
        self.children.append(child)
        self.layout_node.add_child(child.layout_node)
    '''

    def abandon(self, child: Layout) -> None:
        if child not in self.children:
            logger.warning(f"Layout.abandon: not a child: {child.node}")
            return
        self.layout_node.remove_child(child.layout_node)
        self.children.remove(child)
        child.parent = None

    '''
    def abandon(self, child: Layout) -> None:
        self.layout_node.remove_child(child.layout_node)
        self.children.remove(child)
        child.parent = None
    '''

    @property
    def is_root(self) -> bool:
        return self.parent is None

    # -- calculation -------------------------------------------------------

    @property
    def stale(self) -> bool:
        """Whether a recalculation is owed.

        Yoga's own bit, propagated to the root when any descendant is
        dirtied. Named `stale` because `Chip.dirty` is the flush-domain
        flag and this chip has none.
        """
        # ASSUMPTION: is_dirty() is bound. If not, drop the guard at the
        # call site -- calculate on a clean tree early-outs inside yoga.
        return self.layout_node.is_dirty()

    def calculate(
        self,
        width: float = math.nan,
        height: float = math.nan,
        direction: yoga.Direction = yoga.Direction.LTR,
    ) -> None:
        """Recalculate this subtree. Computes only -- nothing is notified.

        `width`/`height` are the available space; nan means unconstrained,
        so the computed size comes from the style.

        Separate from `apply` because the results are readable off this
        chip the moment this returns, and there is at least one caller
        that needs them before the machinery `on_layout` touches exists:
        Window sizes its OS window from a pre-pass run before there is a
        window to resize.

        Root only: an interior chip would compute against a stale parent
        size. Cheap when clean -- yoga early-outs on an undirtied tree.
        """
        if not self.is_root:
            logger.warning(f"Layout.calculate on non-root chip: {self.node}")
            return

        self.layout_node.calculate_bounds(width, height, direction)

    def apply(self) -> None:
        """Push computed results out to every node whose layout changed."""
        if self.layout_node.has_new_layout():
            self.node.on_layout(self)
            self.layout_node.mark_layout_seen()

        # Recurse unconditionally: a child's layout can change while ours
        # does not. The old apply_layout returned early here and never
        # visited the child in that case.
        for child in self.children:
            child.apply()

    # -- style -------------------------------------------------------------

    @property
    def style(self) -> yoga.Style:
        return self.layout_node.get_style()

    @style.setter
    def style(self, value: yoga.Style) -> None:
        if not isinstance(value, yoga.Style):
            raise TypeError(f"Expected yoga.Style, got {type(value)}")
        self.layout_node.set_style(value)

    def set_size(self, width: float, height: float) -> None:
        """Sizing intent. Replaces the old `widget.size = ...` setter."""
        self.layout_node.set_width(width)
        self.layout_node.set_height(height)

    def set_width(self, value: float) -> None:
        self.layout_node.set_width(value)

    def set_height(self, value: float) -> None:
        self.layout_node.set_height(value)

    # -- computed results --------------------------------------------------
    #
    # Yoga's own space: origin top-left, y down, relative to the parent
    # layout node. Nodes convert in on_layout.

    @property
    def left(self) -> float:
        return self.layout_node.get_computed_left()

    @property
    def top(self) -> float:
        return self.layout_node.get_computed_top()

    @property
    def width(self) -> float:
        return self.layout_node.get_computed_width()

    @property
    def height(self) -> float:
        return self.layout_node.get_computed_height()

    @property
    def position(self) -> glm.vec2:
        return glm.vec2(self.left, self.top)

    @property
    def size(self) -> glm.vec2:
        return glm.vec2(self.width, self.height)

    @property
    def parent_size(self) -> glm.vec2:
        """Size of the containing layout, needed to flip into a y-up space.

        A root reports its own size, which makes the flip a no-op there.
        """
        if self.parent is None:
            return self.size
        return self.parent.size

    @property
    def bounds(self) -> yoga.Bounds:
        return self.layout_node.get_computed_bounds()