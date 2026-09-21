from __future__ import annotations

import math
from typing import Iterator

from loguru import logger
import glm

from crunge import yoga

from crunge.core.base_node import BaseNode
from crunge.core.chip import Chip


class Layout[N: BaseNode](Chip[N]):
    """Owns a yoga layout node on behalf of the node it is seated on.

    Two trees, not three. The node tree is the authority on structure and
    order; yoga's tree mirrors it for the nodes that carry a Layout chip.
    The chip itself keeps only a back-pointer to the layout it is linked
    under, never a child list -- children are found by walking the node
    tree, so there is nothing of ours to fall out of sync with it.

    Nodes without a Layout chip are transparent: a chip links to the
    nearest *ancestor* carrying one, and every downward walk here passes
    through layout-less nodes to reach the chips below them. `find_parent`
    goes up that way and `_layout_children` comes down it, so the two
    always agree on who is whose child.

    Calculation is driven from the root; each chip whose computed layout
    changed calls `node.on_layout(self)` and lets the node decide how to
    read the result -- y-down for widgets, y-up for Node2D, y onto z for
    Node3D.

    Dirt is yoga's, not ours. `layout_node` tracks its own dirty bit and
    propagates it to the root, and `has_new_layout()` reports per-node
    staleness after a calculation. A `Dirt` member here would be the
    duplicate source of truth the base class warns about, so this chip
    neither marks nor flushes.

    Specialize by subclassing: `Layout2D(Layout[Node2D])`.
    """

    def __init__(self, style: yoga.Style = None) -> None:
        super().__init__()
        self.layout_node = yoga.LayoutNode()

        config = self.get_config()
        if config is not None:
            self.layout_node.set_config(config)

        self.layout_node.set_style(style or yoga.Style())

        # The layout we are linked under. Not a tree: no child list here.
        self.parent: Layout | None = None

        self._measuring = False
        self._sync_measure_func(leaf=True)

    # -- config ------------------------------------------------------------

    @classmethod
    def get_config(cls) -> yoga.Config | None:
        """Yoga config for this layout's space, or None for yoga's default.

        The setting that matters is the point scale factor, which is what
        yoga rounds computed edges to. The default of 1.0 is right for
        widget space, where a unit is a pixel. It is badly wrong for a
        space measured in metres: every edge rounds to a whole metre, so a
        0.6-unit child comes out 1 unit tall and the one below it, spanning
        0.6 to 1.2, rounds to zero height and lands on top of it.

        Shared per subclass, never destroyed. Config.create is bound under
        return_value_policy::reference, so Python holds a non-owning handle
        and only Config.destroy frees it -- a per-chip config would be pure
        leak, and this one is held for the process lifetime on purpose.
        """
        return None

    # -- attach lifecycle --------------------------------------------------
    #
    # Two entry points for one link, because neither hook alone sees every
    # case. plug covers a node that was already in the tree when its chips
    # were created; on_added covers a node inserted into a tree that already
    # exists. The `parent` guard makes them idempotent, so whichever fires
    # first does the work.

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

    def on_children_sorted(self) -> None:
        """Called after the children of this node have been sorted."""
        self.reorder()

    # -- tree walks --------------------------------------------------------

    def find_parent(self) -> Layout | None:
        """Nearest ancestor node carrying a Layout chip, or None."""
        node = self.node.parent
        while node is not None:
            layout = node.get_chip(Layout)
            if layout is not None:
                return layout
            node = node.parent
        return None

    def _layout_children(self, node: BaseNode | None = None) -> Iterator[Layout]:
        """Layout chips directly below us, in node order.

        The downward mirror of find_parent: descends through layout-less
        nodes and stops at the first chip on each branch, since anything
        below that chip is its child, not ours.

        Yields chips whether or not they have linked yet. Callers that
        need linked children filter on `layout.parent is self` -- during a
        build, siblings further along the node order may not have plugged.
        """
        for child in (node or self.node).children:
            layout = child.get_chip(Layout)
            if layout is not None:
                yield layout
            else:
                yield from self._layout_children(child)

    def _linked_children(self) -> Iterator[Layout]:
        for layout in self._layout_children():
            if layout.parent is self:
                yield layout

    def index_of(self, child: Layout) -> int:
        """Where `child` belongs among our linked children, by node order.

        Counts the linked chips that precede it in the transparent walk.
        `child` itself is not linked yet when this runs, which is why the
        count stops at it rather than finding it among the linked ones.
        """
        index = 0
        for layout in self._layout_children():
            if layout is child:
                return index
            if layout.parent is self:
                index += 1
        # Not below us in the node tree -- find_parent and this walk
        # disagree, which means the node tree changed under us.
        logger.warning(f"Layout.index_of: {child.node} not found below {self.node}")
        return index

    # -- linking -----------------------------------------------------------

    def adopt(self, child: Layout) -> None:
        index = self.index_of(child)
        # Before insert_child, not after: yoga asserts when a node that owns
        # a measure func is given a child, and we are about to stop being a
        # leaf.
        self._sync_measure_func(leaf=False)
        self.layout_node.insert_child(child.layout_node, index)
        child.parent = self

    def abandon(self, child: Layout) -> None:
        if child.parent is not self:
            logger.warning(f"Layout.abandon: not linked here: {child.node}")
            return
        self.layout_node.remove_child(child.layout_node)
        child.parent = None
        # We may be a leaf again, in which case the measure func comes back.
        # ASSUMPTION: get_child_count is bound (YGNodeGetChildCount).
        self._sync_measure_func(leaf=self.layout_node.get_child_count() == 0)

    def reorder(self) -> None:
        """Rebuild yoga's child order from the node tree.

        For after the node tree is reordered in place -- sort_children is
        the case that exists today. Insertion already lands in node order;
        this only matters when the order changes under children that are
        already linked.
        """
        linked = list(self._linked_children())
        for layout in linked:
            self.layout_node.remove_child(layout.layout_node)
        for index, layout in enumerate(linked):
            self.layout_node.insert_child(layout.layout_node, index)

    @property
    def is_root(self) -> bool:
        return self.parent is None

    # -- measurement -------------------------------------------------------

    @property
    def measurable(self) -> bool:
        """Whether the seated node can report its own intrinsic size.

        A measurable leaf answers yoga's sizing question from its own
        content, the way text and images do, instead of being told a size
        from outside. Subclasses that implement `node.on_measure` turn this
        on.
        """
        return False

    def _sync_measure_func(self, leaf: bool) -> None:
        """Install the measure func only while this is a childless leaf.

        Yoga asserts on a node that has both children and a measure func,
        so this is not a one-time setup -- it follows the child count.
        `leaf` is passed in rather than read from yoga because adopt has
        to call this before the child it is about to insert exists there.
        """
        wanted = self.measurable and leaf
        if wanted == self._measuring:
            return

        if wanted:
            self.layout_node.set_measure_func(self._measure)
        else:
            self.layout_node.unset_measure_func()
        self._measuring = wanted

    def _measure(self, width, width_mode, height, height_mode):
        """Yoga's callback. Translates to the node's own terms and back.

        Called several times per pass while flex resolves, so it must stay
        pure: no dirtying, no writing geometry back onto the node. Doing
        either from here is either a reentrancy crash or a dirty loop that
        never settles.
        """
        size = self.node.on_measure(
            width, self._mode(width_mode), height, self._mode(height_mode)
        )
        return yoga.Size(size.x, size.y)

    @staticmethod
    def _mode(mode) -> str:
        """yoga.MeasureMode as a plain string, so nodes need no yoga import."""
        if mode == yoga.MeasureMode.EXACTLY:
            return "exactly"
        if mode == yoga.MeasureMode.AT_MOST:
            return "at_most"
        return "undefined"

    # -- calculation -------------------------------------------------------

    @property
    def stale(self) -> bool:
        """Whether a recalculation is owed.

        Yoga's own bit, propagated to the root when any descendant is
        dirtied. Named `stale` because `Chip.dirty` is the flush-domain
        flag and this chip has none.
        """
        return self.layout_node.is_dirty()

    def calculate(
        self,
        width: float = math.nan,
        height: float = math.nan,
        direction: yoga.Direction = yoga.Direction.LTR,
    ) -> None:
        """Recalculate this subtree. Computes only -- nothing is notified.

        `width`/`height` are the available space; nan means unconstrained,
        so the computed size comes from the style. Pass nan for a root that
        sizes itself: handing it the node's own size looks like a no-op
        today, because an explicitly sized root ignores the available
        space, and becomes circular as soon as anything in the tree is
        sized as a percentage, since that number is the last pass's output.

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
        # does not.
        for layout in self._linked_children():
            layout.apply()

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