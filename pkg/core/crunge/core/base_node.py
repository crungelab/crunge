from __future__ import annotations

from typing import Any, Callable, Self

from loguru import logger

from .base import Base
from .chip import Chip


class BaseNode[T: BaseNode](Base):
    _cls_chips: dict[type, Any] = {}

    '''
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        merged = {}
        for base in reversed(cls.__mro__[1:]):
            merged.update(getattr(base, "_cls_chips", {}))
        cls._cls_chips = merged
    '''
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        merged = {}
        for base in reversed(cls.__mro__[1:]):
            merged.update(getattr(base, "_cls_chips", {}))
        cls._cls_chips = merged

        for name, value in list(vars(cls).items()):
            inject = getattr(value, "inject", None)
            if inject is not None:
                inject(cls, value)

    @classmethod
    def add_cls_chip(cls, chip, key: type | None = None) -> None:
        cls._cls_chips[key or type(chip)] = chip

    @classmethod
    def get_cls_chip(cls, kind: type) -> Any | None:
        return cls._cls_chips.get(kind)

    def get[C: Chip[Any]](self, kind: type[C]) -> C | None:
        chip = self._chip_map.get(kind)
        if chip is not None:
            return chip
        return self._cls_chips.get(kind)

    def has(self, kind: type) -> bool:
        return kind in self._chip_map or kind in self._cls_chips

    """A node in a tree that owns a set of chips.

    Knows nothing about transforms, scenes, or the frame — usable on its
    own for a behaviour-tree task, a pipeline stage, a widget. `Node` adds
    the frame; Node2D/Node3D add the transform.

    Three things live here: the chip set, the tree, and the propagation of
    the Lifetime machine across both. What does not live here is any notion
    of a frame. `Chip.updates`/`draws`/`dispatches` are honoured by `Node`,
    which keeps the pre-filtered broadcast buckets, because only something
    that sits in a scene has a frame to broadcast. A chip seated on a bare
    `BaseNode` is created, plugged, enabled and destroyed like any other —
    but nothing will ever tick, draw or dispatch to it. That is deliberate:
    a node that never renders should not carry three lists that stay empty
    for its whole life.

    The same cut runs through the child walks. `create_children` and its
    siblings are pure lifetime propagation and identical for every kind of
    tree, so they live here. `update_children` and `draw_children` do not —
    a scene ticks every child, a Selector ticks one until it succeeds — so
    per-frame propagation stays with the buckets on `Node`.

    The type parameter is the child type, which is also the self type.
    Every layer stays generic so a subclass can narrow it, and the class
    that nothing extends closes it on itself:

        class Task[T: Task](BaseNode[T]): ...
        class Act(Task["Act"]): ...

    Now `Act().children` is a `list[Act]` and `add_child` rejects anything
    that isn't one. A layer that closes the parameter freezes it for every
    layer below, so close only at the bottom.

    Construction is two passes. `__init__` sets up the node's own state and
    attaches nothing; `seat` attaches chips and returns self, so it reads
    as one expression:

        node = Node2D(position, rotation).seat(SpriteVu(sprite))

    The split is load-bearing. A chip attached inside `Node.__init__` runs
    `on_attached` before `Node2D.__init__` has set up the transform, so any
    chip that reads node state crashes or silently reads a default. By the
    time `seat` runs, every constructor in the MRO has returned.

    A class that always needs a given chip declares it in `_seat` instead,
    which keeps that knowledge in the class rather than at every call site,
    and holds up under subclassing in a way that adding chips at the tail
    of `__init__` does not.

    Seated is not the same as plugged. `seat` puts chips in the board;
    `plug` — driven from `_create`, once the whole set exists and has been
    created — is where each one resolves its siblings.

    Chips are lifetime-owned the same way children are. Chips are walked in
    the lifetime hooks and children in the `*_children` hooks, and since
    `Base` runs `_create` before `create_children` and `destroy_children`
    before `_destroy`, chips are created and enabled before children and
    destroyed after them.
    """

    def __init__(self) -> None:
        super().__init__()

        # Authoritative, insertion-ordered. The only list that sees multiples.
        self._chips: list[Chip[Any]] = []
        # Type -> first instance, populated across the MRO so that
        # require(Mod) finds a SpriteMod.
        self._chip_map: dict[type[Chip[Any]], Chip[Any]] = {}

        self.parent: T | None = None
        self.children: list[T] = []

        self._seated = False
        self._plugged = False

    # -- seating -----------------------------------------------------------

    def seat(self, *chips: Chip[Any]) -> Self:
        """Attach chips. Once, after construction. Returns self.

        Pass a built list with `node.seat(*chips)`.
        """
        if self._seated:
            raise RuntimeError(f"{self!r} is already seated")
        self._seated = True

        for chip in chips:
            self.add(chip)
        self._seat()
        return self

    def _seat(self) -> None:
        """Attach chips this class always needs.

        Runs after the caller's chips, so a default can stand down when the
        caller already supplied one:

            def _seat(self) -> None:
                super()._seat()
                if not self.has(Vu):
                    self.add(SpriteVu())
        """

    @property
    def seated(self) -> bool:
        return self._seated

    # -- chips -------------------------------------------------------------
    def add[C: Chip[Any]](self, chip: C) -> C:
        if self.is_destroying:
            raise RuntimeError(f"cannot add {chip!r} to {self!r} while it tears down")
        if chip._node is not None:
            raise RuntimeError(f"{chip!r} is already attached to {chip._node!r}")

        cls = type(chip)
        self._chips.append(chip)

        # First-wins, per key: multiples stay reachable through get_all(),
        # and get() keeps one unambiguous return type. remove() promotes a
        # successor when a key holder leaves, so a key is never left stale.
        # Filter rather than break on Chip, so mixin order in the subclass
        # can't change which keys land in the map.
        for klass in cls.__mro__:
            if klass is not Chip and issubclass(klass, Chip):
                self._chip_map.setdefault(klass, chip)

        chip.on_attached(self)
        # Late arrival on a live node: bring the chip up to our lifetime and
        # let it resolve the set, which is already complete around it.
        self._sync_lifetime(chip)
        if self._plugged:
            chip.plug()
        return chip

    def remove(self, chip: Chip[Any]) -> None:
        """Detach without destroying. The chip stays created and re-addable;
        the caller owns it from here."""
        if chip not in self._chips:
            raise ValueError(f"{chip!r} is not attached to {self!r}")

        self._chips.remove(chip)

        for klass in type(chip).__mro__:
            if klass is Chip or not issubclass(klass, Chip):
                continue
            if self._chip_map.get(klass) is chip:
                del self._chip_map[klass]
                # Promote the next chip that satisfies this key, if any.
                # Same test add() registers with, so the two agree on what
                # "satisfies" means.
                for candidate in self._chips:
                    if klass in type(candidate).__mro__:
                        self._chip_map[klass] = candidate
                        break

        # Teardown mirrors add() in reverse: enable/plug/create going up,
        # disable/unplug/detach coming down. Disabling first means _disable
        # still has its plugged references.
        chip.disable()
        if self._plugged:
            chip.unplug()
        chip.on_detached()

    '''
    def get[C: Chip[Any]](self, kind: type[C]) -> C | None:
        """One dict hit. Matches subclasses, since the map spans the MRO."""
        return self._chip_map.get(kind)  # type: ignore[return-value]
    '''

    def require[C: Chip[Any]](self, kind: type[C]) -> C:
        chip = self._chip_map.get(kind)
        if chip is None:
            raise KeyError(f"{self!r} has no {kind.__name__}")
        return chip  # type: ignore[return-value]

    def has(self, kind: type) -> bool:
        return kind in self._chip_map

    def get_all[C: Chip[Any]](self, kind: type[C]) -> list[C]:
        """Multiples. Linear over a short list; rare by design."""
        return [c for c in self._chips if isinstance(c, kind)]

    @property
    def chips(self) -> list[Chip[Any]]:
        return self._chips

    @property
    def plugged(self) -> bool:
        return self._plugged

    # -- plugging ----------------------------------------------------------

    def plug(self) -> None:
        """Let every chip resolve its siblings. Driven from _create
        once the whole set exists and has been created."""
        if self._plugged:
            return
        self._plugged = True
        for chip in tuple(self._chips):
            chip.plug()

    def unplug(self) -> None:
        """Drop every cached cross-reference while the set is still intact.
        Reverse order, so late arrivals let go of earlier chips first."""
        if not self._plugged:
            return
        self._plugged = False
        for chip in reversed(tuple(self._chips)):
            chip.unplug()

    # -- lifetime ----------------------------------------------------------
    #
    # Chips in the `_*` hooks, children in the `*_children` hooks. Base
    # interleaves the two, which is what puts chips ahead of children on
    # the way up and behind them on the way down.

    def _create(self) -> None:
        # A caller supplying no extra chips has no reason to call seat, and
        # forgetting it would give a silently empty node. Construction has
        # certainly finished by now, so the two-pass guarantee holds.
        if not self._seated:
            self.seat()
        super()._create()
        for chip in tuple(self._chips):
            chip.create()
        self.plug()

    def create_children(self) -> None:
        super().create_children()
        for child in list(self.children):
            child.create()

    def _enable(self) -> None:
        super()._enable()
        for chip in tuple(self._chips):
            chip.enable()

    def enable_children(self) -> None:
        super().enable_children()
        for child in list(self.children):
            child.enable()

    def _ready(self) -> None:
        super()._ready()
        for chip in tuple(self._chips):
            chip.ready()

    def ready_children(self) -> None:
        #logger.debug(f"Readying children of node: {self}")
        super().ready_children()
        for child in list(self.children):
            child.ready()

    def _disable(self) -> None:
        # No `disable_children` hook to match the others: this mirrors what
        # Node and BaseNode did between them before the merge — children go
        # dark first, then the chips they may still be reading from.
        for child in list(self.children):
            child.disable()
        for chip in reversed(tuple(self._chips)):
            chip.disable()
        super()._disable()

    def destroy_children(self) -> None:
        for child in list(self.children):
            child.destroy()
        self.children.clear()
        super().destroy_children()

    def _destroy(self) -> None:
        logger.debug(f"Destroying node: {self}")
        if self.parent is not None and not self.parent.is_destroying:
            self.parent.remove_child(self)

        # Unplug first: every chip drops its sibling references while the
        # set is whole, so no chip can observe a half-destroyed neighbour.
        self.unplug()
        for chip in reversed(tuple(self._chips)):
            chip.destroy()
            chip.on_detached()

        self._chips.clear()
        self._chip_map.clear()
        self._seated = False
        super()._destroy()

    # -- tree --------------------------------------------------------------

    def add_child(self, child: T) -> T:
        child.parent = self
        self.children.append(child)
        self.on_child_added(child)
        child.on_added()
        self._sync_lifetime(child)
        return child

    def on_child_added(self, child: T) -> None:
        """Parent-side notification. Child is attached but not yet created."""

    def on_added(self) -> None:
        """Self-side notification. Parent is set; lifetime not yet synced."""

    def remove_child(self, child: T) -> None:
        child.disable()
        self.on_child_removed(child)
        child.on_removed()
        child.parent = None
        self.children.remove(child)

    def on_child_removed(self, child: T) -> None:
        """Parent-side notification. Child is disabled but still attached."""

    def on_removed(self) -> None:
        """Self-side notification. Parent is still set."""

    def add_children(self, children: list[T]) -> None:
        for child in children:
            self.add_child(child)

    def remove_children(self, children: list[T]) -> None:
        for child in children:
            self.remove_child(child)

    def clear(self) -> None:
        """Detach all children. They remain created and re-addable."""
        for child in list(self.children):
            self.remove_child(child)

    def sort_children(self, key: Callable[[T], object], reverse: bool = False) -> None:
        """
        Sorts the children list based on a key function.

        :param key: A lambda function that defines the sorting key.
        :param reverse: Whether to sort in reverse order. Default is False.
        """
        self.children.sort(key=key, reverse=reverse)

    def __repr__(self) -> str:
        return (
            f"<{type(self).__name__} chips={len(self._chips)} "
            f"children={len(self.children)}>"
        )