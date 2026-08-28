from __future__ import annotations

from typing import Any, TypeVar

from loguru import logger

from .dispatcher import Dispatcher
from .chip import Chip

C = TypeVar("C", bound=Chip[Any])


class BaseNode(Dispatcher):
    """Owns a set of chips. Knows nothing about hierarchy, transforms, or
    scenes — usable on its own for an app, a widget, a pipeline stage.

    SceneNode adds the graph; Node2D/Node3D add the transform.

    Chips are lifetime-owned the same way children are: the node walks its
    chip set inside the `*_children` hooks, so chips ride the existing
    Lifetime machine rather than a parallel one. Because `BaseNode` sits
    below `Node` in the MRO and the hooks keep the house super-call
    convention (head-call top-down, tail-call bottom-up), chips are created
    and enabled before the vu and children, and destroyed after them.
    """

    def __init__(self, chips: list[Chip[Any]] | None = None) -> None:
        super().__init__()

        # Authoritative, insertion-ordered. The only list that sees multiples.
        self._chips: list[Chip[Any]] = []
        # Type -> first instance, populated across the MRO so that
        # require(Mod) finds a SpriteMod.
        self._chip_map: dict[type, Chip[Any]] = {}
        # Pre-filtered broadcast buckets; no branching in the hot loops.
        self._updatables: list[Chip[Any]] = []
        self._drawables: list[Chip[Any]] = []
        self._dispatchables: list[Chip[Any]] = []

        self._plugged = False

        if chips is not None:
            for chip in chips:
                self.add(chip)

    # -- chips -------------------------------------------------------------

    def add(self, chip: C) -> C:
        if self.is_destroying:  # ASSUMPTION: Base exposes is_destroying
            raise RuntimeError(f"cannot add {chip!r} to {self!r} while it tears down")

        cls = type(chip)
        self._chips.append(chip)

        # First-wins, per key: multiples stay reachable through get_all(),
        # and get() keeps one unambiguous return type. Filter rather than
        # break on Chip, so mixin order in the subclass can't change which
        # keys land in the map.
        for klass in cls.__mro__:
            if klass is not Chip and issubclass(klass, Chip):
                self._chip_map.setdefault(klass, chip)

        if cls.updates:
            self._updatables.append(chip)
        if cls.draws:
            self._drawables.append(chip)
        if cls.dispatches:
            self._dispatchables.append(chip)

        chip.on_attached(self)
        # Late arrival on a live node: bring the chip up to our lifetime and
        # let it resolve the set, which is already complete around it.
        self._sync_lifetime(chip)  # ASSUMPTION: same helper add_child uses
        if self._plugged:
            chip.plug()
        return chip

    def remove(self, chip: Chip[Any]) -> None:
        """Detach without destroying. The chip stays created and re-addable;
        the caller owns it from here."""
        self._chips.remove(chip)
        for bucket in (self._updatables, self._drawables, self._dispatchables):
            if chip in bucket:
                bucket.remove(chip)

        for klass in type(chip).__mro__:
            if klass is Chip or not issubclass(klass, Chip):
                continue
            if self._chip_map.get(klass) is chip:
                del self._chip_map[klass]
                # Promote the next chip that satisfies this key, if any.
                for candidate in self._chips:
                    if isinstance(candidate, klass):
                        self._chip_map[klass] = candidate
                        break

        if self._plugged:
            chip.unplug()
        chip.disable()
        chip.on_detached()

    def get(self, kind: type[C]) -> C | None:
        """One dict hit. Matches subclasses, since the map spans the MRO."""
        return self._chip_map.get(kind)  # type: ignore[return-value]

    def require(self, kind: type[C]) -> C:
        chip = self._chip_map.get(kind)
        if chip is None:
            raise KeyError(f"{self!r} has no {kind.__name__}")
        return chip  # type: ignore[return-value]

    def has(self, kind: type) -> bool:
        return kind in self._chip_map

    def get_all(self, kind: type[C]) -> list[C]:
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
        """Let every chip resolve its siblings. Driven from create_children
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

    def create_children(self) -> None:
        super().create_children()
        for chip in tuple(self._chips):
            chip.create()
        self.plug()

    def enable_children(self) -> None:
        super().enable_children()
        for chip in tuple(self._chips):
            chip.enable()

    def reset_children(self) -> None:
        super().reset_children()
        for chip in tuple(self._chips):
            chip.reset()

    def _disable(self) -> None:
        for chip in reversed(tuple(self._chips)):
            chip.disable()
        super()._disable()

    def destroy_children(self) -> None:
        # Unplug first: every chip drops its sibling references while the
        # set is whole, so no chip can observe a half-destroyed neighbour.
        self.unplug()
        for chip in reversed(tuple(self._chips)):
            chip.destroy()
            chip.on_detached()

        self._chips.clear()
        self._chip_map.clear()
        self._updatables.clear()
        self._drawables.clear()
        self._dispatchables.clear()
        super().destroy_children()

    # -- broadcasts (self only; Node walks the tree) -----------------------

    def _update(self, delta_time: float) -> None:
        for chip in self._updatables:
            chip.update(delta_time)

    def _draw(self) -> None:
        for chip in self._drawables:
            chip.draw()

    def dispatch(self, event: Any) -> bool:
        """First chip to claim the event wins."""
        for chip in self._dispatchables:
            if chip.dispatch(event):
                return True
        return super().dispatch(event)

    def __repr__(self) -> str:
        return f"<{type(self).__name__} chips={len(self._chips)}>"