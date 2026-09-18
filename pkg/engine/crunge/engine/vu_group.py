from __future__ import annotations

from typing import Any, List

from loguru import logger

from .render_state import RenderState
from .vu import Vu

ELEMENTS = 32


class Run:
    """One draw's worth of contiguous slots.

    Opaque to the RenderGroup, which only ever asks the owning group to
    extend one or draw it. Subclasses carry whatever else that group needs
    at bind time.
    """

    __slots__ = ("first", "count")

    def __init__(self, first: int) -> None:
        self.first = first
        self.count = 1

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: first={self.first} count={self.count}>"


class VuGroup[VuT: Vu]:
    """A binding unit: members, slot order, and the runs they cut into.

    Deliberately free of GPU and dimension-specific types. `engine.node`
    imports `engine.render_group`, which imports this — and `engine.d2`
    imports `engine.node` back, so anything reaching into d2 from here
    closes a cycle at import time. The node buffer and its bind group live
    in VuGroup2D, on the other side of that edge, where both are visible.

    Not a chip. The RenderGroup owns it and drives it, so the chip walk
    reaches the whole arrangement exactly once.

    Membership order is not draw order. A group does not know where its
    members sit in the global sequence — the RenderGroup assigns that, and
    the slot, because both are decisions across every group at once.
    """

    def __init__(self, count: int = ELEMENTS, program=None) -> None:
        self.count = count
        self.program = program
        self.members: List[VuT] = []
        self.is_created = False

    # -- identity ----------------------------------------------------------

    @property
    def key(self) -> Any:
        """What the RenderGroup routes on."""
        return self.__class__

    @property
    def full(self) -> bool:
        return len(self.members) >= self.count

    # -- lifetime ----------------------------------------------------------

    def ensure_created(self) -> None:
        """Bring GPU resources up.

        On demand rather than from a create pass, because groups are
        instantiated when their first vu enables and when an existing group
        spills — both long after _create has swept through.
        """
        if self.is_created:
            return
        self.is_created = True
        self._create()

    def _create(self) -> None:
        pass

    def destroy(self) -> None:
        self.clear()
        self.is_created = False

    # -- membership --------------------------------------------------------

    def append(self, vu: VuT) -> None:
        if vu in self.members:
            raise ValueError(f"{vu} already in {self}")
        if self.full:
            raise IndexError(
                f"{self} is full ({self.count}); routing should have spilled"
            )
        self.members.append(vu)
        # Last: the setter fires on_group. A subclass assigning buffer state
        # after this returns is fine — the vu marks dirt and the write lands
        # on the next flush.
        vu.group = self


    def remove(self, vu: VuT) -> None:
        self.members.remove(vu)
        vu.group = None

    def clear(self) -> None:
        for vu in tuple(self.members):
            self.remove(vu)

    def __len__(self) -> int:
        return len(self.members)

    def __iter__(self):
        return iter(self.members)

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}: {len(self)}/{self.count}>"

    # -- planning ----------------------------------------------------------

    def ready(self, vu: VuT) -> bool:
        """Can this vu be placed and batched yet?

        A vu can be appended before its model arrives. Until it does there is
        no material to batch on, so it gets no slot and does not draw.
        """
        return True

    def sort_key(self, vu: VuT) -> Any:
        """Global ordering key.

        Compared against every other group's keys in the same RenderGroup,
        so keep the shape fixed across groups — and make sure it carries the
        whole ordering, since the RenderGroup collects entries group by
        group and has nothing else to fall back on.

        Append sequence is the safe default: it reproduces whatever ordering
        the caller already established.
        """
        return vu.group_sequence

    def place(self, vu: VuT, slot: int) -> None:
        """Assign a buffer slot. Subclasses know what a slot is."""
        raise NotImplementedError

    def new_run(self, vu: VuT, first: int) -> Run:
        return Run(first)

    def extends(self, run: Run, vu: VuT) -> bool:
        """May `vu` join `run`?

        Only asked when `vu` is the next slot in this same group, so
        contiguity is already established — this decides material identity,
        nothing more. Merging adjacent equal materials never reorders
        anything, so it is always safe.
        """
        return False

    # -- frame -------------------------------------------------------------

    def update(self, delta_time: float) -> None:
        for vu in self.members:
            vu.update(delta_time)

    def draw_run(self, state: RenderState, run: Run) -> None:
        raise NotImplementedError