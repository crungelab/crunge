from __future__ import annotations

from typing import Any, ClassVar
from bisect import insort

from crunge.core.signal import Signal
from crunge.core.base_node import BaseNode
from crunge.core.chip import Chip
from .vu import Vu
from .controller import Controller

from .model import Model


class Node[T: Node](BaseNode[T]):
    vu_class: ClassVar[type[Vu] | None] = None
    controller_class: ClassVar[type[Controller] | None] = None

    """A node in the scene graph.

    `BaseNode` gives the chip set, the tree, and lifetime propagation over
    both. What `Node` adds is the frame: the pre-filtered broadcast buckets
    — `_updatables`, `_drawables`, `_dispatchables` — and the per-frame
    walks over children that go with them.

    Those walks stay here rather than moving up because they are not shared.
    A scene ticks and draws every child; a behaviour-tree composite ticks
    one child until it succeeds. Only the lifetime walks are common to every
    tree, and those are already upstairs.

    Maintaining the buckets is `add`/`remove`'s job, layered over BaseNode's:
    BaseNode owns membership and type lookup, Node files each chip into
    whichever buckets its class declares.

    The vu is a chip like any other — creation, enabling, drawing, updating
    and teardown all come from the chip walk in BaseNode. `vu` is kept as a
    named accessor onto the chip map, since that is how most call sites want
    to talk about it.

    Chips are attached with `seat`, never in the constructor:

        node = Node2D(position, rotation).seat(SpriteVu(sprite))
    """

    def __init__(self, model: "Model | None" = None) -> None:
        super().__init__()
        self._model: "Model | None" = None

        # Pre-filtered broadcast buckets; no branching in the hot loops.
        # Subsets of BaseNode._chips, which stays authoritative.
        self._updatables: list[Chip[Any]] = []
        self._drawables: list[Chip[Any]] = []
        self._dispatchables: list[Chip[Any]] = []

        # TODO: transform_changed belongs on Node2D/Node3D. Node has no
        # transform, so a chip that connects here on a plain Node is
        # listening to a signal that can never fire.
        self.transform_changed: Signal[Node[T]] = Signal()
        self.model_changed: Signal[Node[T]] = Signal()

        # Safe in __init__: the model is this class's own state, and there
        # are no subscribers yet. A chip mounted later picks it up through
        # connect_now.
        self.model = model
        self.visible = True

    def _seat(self) -> None:
        super()._seat()
        if self.vu_class is not None:
            self.add(self.vu_class())
        if self.controller_class is not None:
            self.add(self.controller_class())

    # -- chips -------------------------------------------------------------
    #
    # BaseNode decides membership; Node decides what each chip is broadcast
    # to.

    def add[C: Chip[Any]](self, chip: C) -> C:
        chip = super().add(chip)

        # Bucketed after super(), which means after on_attached and any
        # plug: update_order can be settled from node or sibling state and
        # still land in the right slot. Nothing broadcasts inside add, so
        # the chip cannot miss a tick by being filed a few lines late.
        cls = type(chip)
        if cls.updates:
            insort(self._updatables, chip, key=lambda chip: chip.update_order)
        if cls.draws:
            self._drawables.append(chip)
        if cls.dispatches:
            self._dispatchables.append(chip)
        return chip

    def remove(self, chip: Chip[Any]) -> None:
        # Mirror of add: out of the buckets first, so the chip is off every
        # broadcast list before super() disables and unplugs it. A chip that
        # was never attached is in no bucket, so the guard in super() still
        # gets to raise on a clean object.
        for bucket in (self._updatables, self._drawables, self._dispatchables):
            if chip in bucket:
                bucket.remove(chip)
        super().remove(chip)

    # -- properties --------------------------------------------------------

    # Model property
    @property
    def model(self) -> "Model | None":
        return self._model

    @model.setter
    def model(self, value: "Model | None") -> None:
        self._model = value
        if value is None:
            return
        self.model_changed.emit(self)

    # Vu property
    @property
    def vu(self) -> Vu | None:
        return self.get(Vu)

    @vu.setter
    def vu(self, value: Vu | None) -> None:
        old = self.get(Vu)
        if old is value:
            return
        if old is not None:
            self.remove(old)
            old.destroy()
        if value is not None:
            self.add(value)

    # Controller property
    @property
    def controller(self) -> Controller | None:
        return self.get(Controller)

    @controller.setter
    def controller(self, value: Controller | None) -> None:
        old = self.get(Controller)
        if old is value:
            return
        if old is not None:
            self.remove(old)
            old.destroy()
        if value is not None:
            self.add(value)

    # -- lifetime ----------------------------------------------------------

    def _destroy(self) -> None:
        super()._destroy()
        # After super(), which has already destroyed and detached every
        # chip. These are the last references the node holds to them.
        self._updatables.clear()
        self._drawables.clear()
        self._dispatchables.clear()

    # -- frame -------------------------------------------------------------
    #
    # `_draw`, `_update` and `dispatch` broadcast to this node's own chips;
    # `draw`, `update` and the child walks carry it down the tree.

    def _draw(self) -> None:
        for chip in self._drawables:
            chip.draw()

    def draw(self) -> None:
        if not self.visible:
            return
        self._draw()
        self.draw_children()

    def draw_children(self) -> None:
        for child in self.children:
            self.draw_child(child)

    def draw_child(self, child: T) -> None:
        child.draw()

    def render(self) -> None:
        self.draw()

    def _update(self, delta_time: float) -> None:
        for chip in self._updatables:
            chip.update(delta_time)

    def update(self, delta_time: float) -> None:
        self._update(delta_time)
        self.update_children(delta_time)

    def update_children(self, delta_time: float) -> None:
        for child in self.children:
            self.update_child(child, delta_time)

    def update_child(self, child: T, delta_time: float) -> None:
        child.update(delta_time)

    def dispatch(self, event: Any) -> bool:
        """First chip to claim the event wins."""
        for chip in self._dispatchables:
            if chip.dispatch(event):
                return True
        return super().dispatch(event)